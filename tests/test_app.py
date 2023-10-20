# import json
# import os
#
# import pytest
# from chalice.test import Client
#
#
# @pytest.fixture
# def env():
#     while "app.py" not in os.listdir():
#         os.chdir("..")
#     import dotenv
#
#     dotenv.load_dotenv()
#
#     # Load .chalice/config.json
#     import json
#
#     with open(".chalice/config.json", "r") as fd:
#         config = json.load(fd)
#
#     env = config.get("environment_variables", {})
#     env.update(
#             config.get("stages", {}).get("dev_v1", {}).get("environment_variables", {})
#     )
#     os.environ.update(env)
#
#
# @pytest.fixture
# def client(env):
#     from app import app
#
#     with Client(app, stage_name="dev_v1") as client:
#         yield client
#
#
# @pytest.fixture
# def message():
#     return {
#         "date": "2023-11-11",
#         "origin": "transform",
#         "rel_name": "products",
#         "db_name": "service_dev",
#         "data": ['etl-transform/products_0.json', 'etl-transform/products_1.json', 'etl-transform/products_2.json',
#                  'etl-transform/products_3.json', 'etl-transform/products_4.json', 'etl-transform/products_5.json',
#                  'etl-transform/products_6.json', 'etl-transform/products_7.json', 'etl-transform/products_8.json',
#                  'etl-transform/products_9.json', 'etl-transform/products_10.json', 'etl-transform/products_11.json',
#                  'etl-transform/products_12.json', 'etl-transform/products_13.json', 'etl-transform/products_14.json',
#                  'etl-transform/products_15.json', 'etl-transform/products_16.json', 'etl-transform/products_17.json',
#                  'etl-transform/products_18.json', 'etl-transform/products_19.json', 'etl-transform/products_20.json',
#                  'etl-transform/products_21.json', 'etl-transform/products_22.json', 'etl-transform/products_23.json',
#                  'etl-transform/products_24.json', 'etl-transform/products_25.json', 'etl-transform/products_26.json',
#                  'etl-transform/products_27.json', 'etl-transform/products_28.json', 'etl-transform/products_29.json',
#                  'etl-transform/products_30.json', 'etl-transform/products_31.json', 'etl-transform/products_32.json',
#                  'etl-transform/products_33.json', 'etl-transform/products_34.json', 'etl-transform/products_35.json',
#                  'etl-transform/products_36.json', 'etl-transform/products_37.json', 'etl-transform/products_38.json',
#                  'etl-transform/products_39.json', 'etl-transform/products_40.json', 'etl-transform/products_41.json',
#                  'etl-transform/products_42.json', 'etl-transform/products_43.json', 'etl-transform/products_44.json',
#                  'etl-transform/products_45.json', 'etl-transform/products_46.json', 'etl-transform/products_47.json',
#                  'etl-transform/products_48.json', 'etl-transform/products_49.json', 'etl-transform/products_50.json',
#                  'etl-transform/products_51.json', 'etl-transform/products_52.json', 'etl-transform/products_53.json',
#                  'etl-transform/products_54.json', 'etl-transform/products_55.json', 'etl-transform/products_56.json',
#                  'etl-transform/products_57.json', 'etl-transform/products_58.json', 'etl-transform/products_59.json',
#                  'etl-transform/products_60.json', 'etl-transform/products_61.json', 'etl-transform/products_62.json',
#                  'etl-transform/products_63.json', 'etl-transform/products_64.json', 'etl-transform/products_65.json',
#                  'etl-transform/products_66.json', 'etl-transform/products_67.json', 'etl-transform/products_68.json',
#                  'etl-transform/products_69.json', 'etl-transform/products_70.json', 'etl-transform/products_71.json',
#                  'etl-transform/products_72.json', 'etl-transform/products_73.json', 'etl-transform/products_74.json',
#                  'etl-transform/products_75.json', 'etl-transform/products_76.json', 'etl-transform/products_77.json',
#                  'etl-transform/products_78.json', 'etl-transform/products_79.json', 'etl-transform/products_80.json',
#                  'etl-transform/products_81.json', 'etl-transform/products_82.json', 'etl-transform/products_83.json',
#                  'etl-transform/products_84.json', 'etl-transform/products_85.json', 'etl-transform/products_86.json',
#                  'etl-transform/products_87.json', 'etl-transform/products_88.json', 'etl-transform/products_89.json',
#                  'etl-transform/products_90.json', 'etl-transform/products_91.json', 'etl-transform/products_92.json',
#                  'etl-transform/products_93.json', 'etl-transform/products_94.json', 'etl-transform/products_95.json',
#                  'etl-transform/products_96.json', 'etl-transform/products_97.json', 'etl-transform/products_98.json',
#                  'etl-transform/products_99.json', 'etl-transform/products_100.json',
#                  'etl-transform/products_updated.json']
#     }
#
#
# def test_send(client, message):
#     response = client.lambda_.invoke(
#             "upsert",
#             client.events.generate_sqs_event(
#                     queue_name=os.getenv("QUEUE_NAME"),
#                     message_bodies=[json.dumps(message, ensure_ascii=False)],
#             ),
#     )
#     assert response.payload != {}
