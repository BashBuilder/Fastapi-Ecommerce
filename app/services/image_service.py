import secrets
from pathlib import Path
from typing import Annotated

import anyio
from fastapi import File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError


async def create_upload_file(
  file: Annotated[UploadFile, File(...)],
) -> str:
  filepath = Path("static/images")
  filepath.mkdir(parents=True, exist_ok=True)

  if not file.filename:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Filename is required.",
    )

  extension = Path(file.filename).suffix.lower().lstrip(".")

  if extension not in {"jpg", "jpeg", "png"}:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid file type. Only jpg, jpeg, and png are allowed.",
    )

  token_name = f"{secrets.token_hex(16)}.{extension}"
  generated_path = filepath / token_name

  contents = await file.read()

  try:
    await anyio.to_thread.run_sync(
      _process_image,
      contents,
      generated_path,
    )
  except (UnidentifiedImageError, OSError) as exc:
    generated_path.unlink(missing_ok=True)
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="The uploaded file is not a valid image.",
    ) from exc

  return generated_path.as_posix()


def _process_image(contents: bytes, path: Path) -> None:
  from io import BytesIO

  with Image.open(BytesIO(contents)) as image:
    image = image.convert("RGB")
    image = image.resize((200, 200), Image.Resampling.LANCZOS)  # type: ignore
    image.save(path, format="JPEG", quality=90)
