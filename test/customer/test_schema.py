# import uuid
# from faker import Faker
# from pydantic import ValidationError
# import pytest
# from src.app. user import schema


# # def test_ICustomerIn(faker: Faker):
# #     data = dict(
# #         firstname=faker.first_name(),
# #         lastname=faker.last_name(),
# #         email=faker.email(),
# #         username=faker.user_name(),
# #         password=faker.password(),
# #     )
# #     data_in = schema.ICustomerIn(**data)
# #     assert data_in.construct()
# #     assert data_in.dict().keys() == data.keys()


# def test_ICustomerIn_bad_data(faker: Faker):
#     with pytest.raises(ValidationError):
#         data = dict(
#             firstname=faker.first_name(),
#             lastname=faker.last_name(),
#             email=faker.email(),
#             password=faker.password(),
#         )
#         data_in = schema.ICustomerIn(**data)
#         assert data_in.construct()
#         assert data_in.dict().keys() == data.keys()


# def test_ICustomerOut_bad_data(faker: Faker):
#     with pytest.raises(ValidationError):
#         data = dict(
#             firstname=faker.first_name(),
#             lastname=faker.last_name(),
#             email=faker.email(),
#             username=faker.user_name(),
#             password=faker.password(),
#         )
#         data_in = schema.ICustomerOut(**data)
#         assert data_in.construct()
#         assert data_in.dict().keys() == data.keys()


# def test_ICustomerOut(faker: Faker):
#     data = dict(
#         id=uuid.uuid4(),
#         firstname=faker.first_name(),
#         lastname=faker.last_name(),
#         email=faker.email(),
#         username=faker.user_name(),
#         is_active=True,
#         is_suspended=False,
#         is_verified=False,
#     )
#     data_in = schema.ICustomerOut(**data)
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_ICustomerOutFull(faker: Faker):
#     data = dict(
#         id=str(uuid.uuid4()),
#         firstname=faker.first_name(),
#         lastname=faker.last_name(),
#         email=faker.email(),
#         username=faker.user_name(),
#         is_active=True,
#         is_suspended=False,
#         is_verified=False,
#         permissions=[str(uuid.uuid4())],
#     )

#     data_in = schema.ICustomerOutFull(**data)
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_IGetPasswordResetLink(faker: Faker):
#     data = dict(email=faker.email())
#     data_in = schema.IGetPasswordResetLink(email=faker.email())
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_ICustomerAccountVerifyToken(faker: Faker):
#     data = dict(token=faker.lexify(text="Random Identifier: ??????????"))
#     data_in = schema.ICustomerAccountVerifyToken(
#         token=faker.lexify(text="Random Identifier: ??????????")
#     )
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_ICustomerResetForgetPassword(faker: Faker):
#     data = dict(email=faker.email())
#     data_in = schema.ICustomerResetForgetPassword(email=faker.email())
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_ICustomerRoleUpdate():
#     data = dict(users_id=str(uuid.uuid4()), permissions=[str(uuid.uuid4())])
#     data_in = schema.ICustomerRoleUpdate(
#         users_id=str(uuid.uuid4()), permissions=[str(uuid.uuid4())]
#     )
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()


# def test_ICustomerRemove():
#     data = dict(users_id=str(uuid.uuid4()), permanent=True)
#     data_in = schema.ICustomerRemove(users_id=str(uuid.uuid4()), permanent=True)
#     assert data_in.construct()
#     assert data_in.dict().keys() == data.keys()
