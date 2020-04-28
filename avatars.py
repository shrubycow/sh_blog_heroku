import os

base_dir = os.getcwd()
avatar_dir = os.path.join(base_dir, 'static', 'accounts', 'avatars')
print(avatar_dir)
files_list = []
for root, dirs, files in os.walk(avatar_dir):
    files_list = files

for num, file in enumerate(files_list):
    files_list[num] = 'accounts/avatars/'+file

print(files_list)