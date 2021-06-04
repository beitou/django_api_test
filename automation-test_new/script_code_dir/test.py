import json
a={"15175036183":"8cd91db86cb548ca9a052fdb2e431b68"}
# result=json.dumps(a)
# print(result)
# print(type(result))


b = json.loads(a)
for key in a :
    print(key)
    print(a[key])