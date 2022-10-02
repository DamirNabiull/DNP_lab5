# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chord.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63hord.proto\"\x07\n\x05\x45mpty\"/\n\x0fRegisterRequest\x12\x0e\n\x06ipaddr\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\")\n\x10RegisterResponse\x12\n\n\x02id\x18\x01 \x01(\x03\x12\t\n\x01m\x18\x02 \x01(\x05\"\x1f\n\x11\x44\x65registerRequest\x12\n\n\x02id\x18\x01 \x01(\x03\"5\n\x12\x44\x65registerResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"(\n\x1aPopulateFingerTableRequest\x12\n\n\x02id\x18\x01 \x01(\x03\"+\n\x0cNodeInfoItem\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\"(\n\x0bSaveRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\" \n\x11\x46indRemoveRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"5\n\x12NodeActionResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xc0\x01\n\x0fRegistryService\x12/\n\x08register\x12\x10.RegisterRequest\x1a\x11.RegisterResponse\x12\x35\n\nderegister\x12\x12.DeregisterRequest\x1a\x13.DeregisterResponse\x12\x45\n\x15populate_finger_table\x12\x1b.PopulateFingerTableRequest\x1a\r.NodeInfoItem0\x01\x32\x42\n\x15RegistryClientService\x12)\n\x0eget_chord_info\x12\x06.Empty\x1a\r.NodeInfoItem0\x01\x32\xc9\x01\n\x0bNodeService\x12+\n\x10get_finger_table\x12\x06.Empty\x1a\r.NodeInfoItem0\x01\x12)\n\x04save\x12\x0c.SaveRequest\x1a\x13.NodeActionResponse\x12\x31\n\x06remove\x12\x12.FindRemoveRequest\x1a\x13.NodeActionResponse\x12/\n\x04\x66ind\x12\x12.FindRemoveRequest\x1a\x13.NodeActionResponseb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_REGISTERREQUEST = DESCRIPTOR.message_types_by_name['RegisterRequest']
_REGISTERRESPONSE = DESCRIPTOR.message_types_by_name['RegisterResponse']
_DEREGISTERREQUEST = DESCRIPTOR.message_types_by_name['DeregisterRequest']
_DEREGISTERRESPONSE = DESCRIPTOR.message_types_by_name['DeregisterResponse']
_POPULATEFINGERTABLEREQUEST = DESCRIPTOR.message_types_by_name['PopulateFingerTableRequest']
_NODEINFOITEM = DESCRIPTOR.message_types_by_name['NodeInfoItem']
_SAVEREQUEST = DESCRIPTOR.message_types_by_name['SaveRequest']
_FINDREMOVEREQUEST = DESCRIPTOR.message_types_by_name['FindRemoveRequest']
_NODEACTIONRESPONSE = DESCRIPTOR.message_types_by_name['NodeActionResponse']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)

RegisterRequest = _reflection.GeneratedProtocolMessageType('RegisterRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERREQUEST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:RegisterRequest)
  })
_sym_db.RegisterMessage(RegisterRequest)

RegisterResponse = _reflection.GeneratedProtocolMessageType('RegisterResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERRESPONSE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:RegisterResponse)
  })
_sym_db.RegisterMessage(RegisterResponse)

DeregisterRequest = _reflection.GeneratedProtocolMessageType('DeregisterRequest', (_message.Message,), {
  'DESCRIPTOR' : _DEREGISTERREQUEST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:DeregisterRequest)
  })
_sym_db.RegisterMessage(DeregisterRequest)

DeregisterResponse = _reflection.GeneratedProtocolMessageType('DeregisterResponse', (_message.Message,), {
  'DESCRIPTOR' : _DEREGISTERRESPONSE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:DeregisterResponse)
  })
_sym_db.RegisterMessage(DeregisterResponse)

PopulateFingerTableRequest = _reflection.GeneratedProtocolMessageType('PopulateFingerTableRequest', (_message.Message,), {
  'DESCRIPTOR' : _POPULATEFINGERTABLEREQUEST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:PopulateFingerTableRequest)
  })
_sym_db.RegisterMessage(PopulateFingerTableRequest)

NodeInfoItem = _reflection.GeneratedProtocolMessageType('NodeInfoItem', (_message.Message,), {
  'DESCRIPTOR' : _NODEINFOITEM,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:NodeInfoItem)
  })
_sym_db.RegisterMessage(NodeInfoItem)

SaveRequest = _reflection.GeneratedProtocolMessageType('SaveRequest', (_message.Message,), {
  'DESCRIPTOR' : _SAVEREQUEST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:SaveRequest)
  })
_sym_db.RegisterMessage(SaveRequest)

FindRemoveRequest = _reflection.GeneratedProtocolMessageType('FindRemoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINDREMOVEREQUEST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:FindRemoveRequest)
  })
_sym_db.RegisterMessage(FindRemoveRequest)

NodeActionResponse = _reflection.GeneratedProtocolMessageType('NodeActionResponse', (_message.Message,), {
  'DESCRIPTOR' : _NODEACTIONRESPONSE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:NodeActionResponse)
  })
_sym_db.RegisterMessage(NodeActionResponse)

_REGISTRYSERVICE = DESCRIPTOR.services_by_name['RegistryService']
_REGISTRYCLIENTSERVICE = DESCRIPTOR.services_by_name['RegistryClientService']
_NODESERVICE = DESCRIPTOR.services_by_name['NodeService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=15
  _EMPTY._serialized_end=22
  _REGISTERREQUEST._serialized_start=24
  _REGISTERREQUEST._serialized_end=71
  _REGISTERRESPONSE._serialized_start=73
  _REGISTERRESPONSE._serialized_end=114
  _DEREGISTERREQUEST._serialized_start=116
  _DEREGISTERREQUEST._serialized_end=147
  _DEREGISTERRESPONSE._serialized_start=149
  _DEREGISTERRESPONSE._serialized_end=202
  _POPULATEFINGERTABLEREQUEST._serialized_start=204
  _POPULATEFINGERTABLEREQUEST._serialized_end=244
  _NODEINFOITEM._serialized_start=246
  _NODEINFOITEM._serialized_end=289
  _SAVEREQUEST._serialized_start=291
  _SAVEREQUEST._serialized_end=331
  _FINDREMOVEREQUEST._serialized_start=333
  _FINDREMOVEREQUEST._serialized_end=365
  _NODEACTIONRESPONSE._serialized_start=367
  _NODEACTIONRESPONSE._serialized_end=420
  _REGISTRYSERVICE._serialized_start=423
  _REGISTRYSERVICE._serialized_end=615
  _REGISTRYCLIENTSERVICE._serialized_start=617
  _REGISTRYCLIENTSERVICE._serialized_end=683
  _NODESERVICE._serialized_start=686
  _NODESERVICE._serialized_end=887
# @@protoc_insertion_point(module_scope)
