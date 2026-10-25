# async def create_business(
#   sender: type[User],
#   instance: User,
#   created: bool,
#   using_db: BaseDBAsyncClient | None,
#   update_fields: list[str] | None,
# ) -> None:
#   if not created:
#     return

#   await Business.create(
#     business_name=instance.username,
#     owner=instance,
#     using_db=using_db,
#   )


# post_save(User)(create_business)
