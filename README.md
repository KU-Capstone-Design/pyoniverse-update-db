# Pyoniverse Update DB
> Service DB를 갱신하는 모든 작업이 처리됨
## Description
- 서비스의 일부분(API, Dashboard 등)에서 Service DB를 직접 갱신하지 않는다.
- 모든 업데이트는 이 서비스로 Message를 보냄으로써 처리된다.
- ORIGIN이 추가되거나 새로운 행위가 필요하면 이 서비스에 ORIGIN, ACTION을 추가하고, Message를 보낸다.
## Documentations
- [architecture](doc/architecture.md)
