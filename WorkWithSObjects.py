#!/usr/bin/python

import os
import re
import PackageCreator

s_objects_path = '.\\sample\\retrieveSObjects\\objects'
map_s_object_and_lookup_fields = {}

regexp_find_lookup_fields = '(?<=<fullName>)([a-zA-Z0-9_]+)(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>)'
regexp_find_s_object_name_from_file_name = '.*?(?=\.)'


def get_lookup_fields():
    s_objects_dir = os.listdir(path=s_objects_path)
    if len(s_objects_dir) > 0:
        os.chdir(s_objects_path)
        for s_object_file in s_objects_dir:
            s_object_name = re.search(regexp_find_s_object_name_from_file_name, s_object_file).group(0)
            with open(s_object_file, "r") as file:
                look_up_fields = re.findall(regexp_find_lookup_fields, file.read(), re.M | re.S)
                if look_up_fields is not None:
                    map_s_object_and_lookup_fields[s_object_name] = look_up_fields
    print(map_s_object_and_lookup_fields)


if __name__ == "__main__":
    get_lookup_fields()



#(AccountCId__c|ContactCId__c)<\/leftValueReference>\n\s{16}<operator>IsNull<\/operator>\n\s{16}<rightValue>\n\s{20}<booleanValue>true regexp для нахождения условия что Lookup field is null
