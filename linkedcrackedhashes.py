# A Python script that automates the linking of cracked passwords from Hashcat to the raw NTLM (NTDS.dit) dump from Secretsdump. 
# This was created as an alternative to the Excel method to map the output of the two tools as presented in TCM Security's PEH course (Dumping the NTDS.dit).
# By @unclesocks

import pprint
from argparse import ArgumentParser


def parse_ntlm_dump(file):
    ntlm_list = []
    try:
        with open(file) as ntlm_dump:
            for ntlm in ntlm_dump:
                sections = ntlm.strip().split(":")
                if len(sections) >=4:
                    user, rid, lm_hash, nt_hash = sections[:4]                   
                    ntlm_list.append({
                        "Domain/Username":user, 
                        "RID":rid, 
                        "LMHash":lm_hash,
                        "NTHash":nt_hash, 
                        "Password":""
                    })
                    
    except:
        raise ValueError(f"Error in opening or parsing NTLM dump file - {Exception}")
    return ntlm_list


def parse_cracked_dump(file):
    cracked_dict = {}
    try:
        with open(file) as cracked_pw:
            for pw in cracked_pw:
                if pw.strip():
                    nt_hash, password, *_ = pw.split(":", 1)
                    cracked_dict[nt_hash] = str(password if password else "")

    except:
        raise ValueError(f"Error in opening or parsing cracked password file - {Exception}")
    return cracked_dict


def link_cracked_pw(ntlm_list, cracked_dict):  
    for ntlm in ntlm_list:
        nt_hash = ntlm["NTHash"]
        ntlm["Password"] = cracked_dict.get(nt_hash, "").strip()

    return ntlm_list


if __name__ == "__main__":
    arg_parse = ArgumentParser(description="Links cracked passsword hashes from Hashcat with raw NTLM dump from SecretsDump.")
    arg_parse.add_argument("-n", "--ntlm", help="Raw NTLM dump file location.")
    arg_parse.add_argument("-c", "--cracked", help="Cracked password file location.")
    args = arg_parse.parse_args()

    ntlm_file = args.ntlm
    cracked_file = args.cracked

    if not ntlm_file or not cracked_file:
        raise ValueError("-n and -c options are required.")
    
    ntlm_list = parse_ntlm_dump(ntlm_file)
    cracked_list = parse_cracked_dump(cracked_file)
    output = link_cracked_pw(ntlm_list, cracked_list)
    pprint.pprint(output, sort_dicts=False)
