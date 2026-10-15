# LinkCrackedHashes
A Python script that automates the linking of cracked passwords from Hashcat to the raw NTLM (NTDS.dit) dump from Secretsdump. This was created as an alternative to the Excel method to map the output of the two tools as presented in TCM Security's PEH course (Dumping the NTDS.dit).

## Tool Usage

Users need to specify the raw Secretsdump NTLM (domain\uid:rid:lmhash:nthash) and Hashcat cracked password output (--show) text files using the -n and -c options, respectively. The output will be in JSON format.

**Kali Linux (Example):**

```python3 linkcrackedhashes.py -n "/path/to/ntlmDump.txt" -c "/path/to/hashcatCrackPws.txt"```

<img width="869" height="284" alt="image" src="https://github.com/user-attachments/assets/9b821e57-b4a6-4145-8971-62335c92deb3" />
