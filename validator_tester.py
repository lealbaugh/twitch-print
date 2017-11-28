import re

dewey_validator=re.compile(r"([a-zA-Z]{1,3}\s*[\d\.]{1,7}\s*\.[a-zA-Z]\d{1,5}\s*[\w]{2,4}\s*\d{0,4}|(STACKS|OVRSZQ)[\-2-4]{0,2})")

test_string = "PN6110 .C3 C38 2014, Hunt Library - STACKS-2\nZ1033 .M6 M43X NO. 37, Hunt Library - SPEC-MIN-4\nQH442.6 .A58 2013, Qatar Library - Q-POPULAR\nPS3607 .R27 C87 2010, Hunt Library - STACKS-2\nHD9757 .N3 M34 2009, Hunt Library - STACKS-2\nN6973 .B54 A4 2016, Hunt Library - OVRSZQ-4\nDS557.7 .L376 2002, Hunt Library - STACKS-2\nPS3568 .O2383 E44 2003, Hunt Library - STACKS-2\nPR6053 .O986 H47 2011, Hunt Library - STACKS-2\nPS3552 .R698 C37 2010, Hunt Library - STACKS-2\nN6853 .B3 A4 2013, Hunt Library - STACKS-4\nPR6119 .T736 P37 2011, Hunt Library - STACKS-2\nSF442.82 .B68 A3 2013, Hunt Library - STACKS-3\nPS3603 .R685 C67 2005, Hunt Library - STACKS-2\nPS1331 .R57 2007, Hunt Library - STACKS-2\nPS3575 .O633 R5 2008, Hunt Library - STACKS-2\nB3148 .M34 2006, Hunt Library - STACKS-2"
# for message in test_string.split("\n"):
# 	for match in dewey_validator.findall(message):
# 		for chunk in match:
# 			if (chunk):
# 				print(chunk)
# 		print("-----------")
# 	print("--------------------------------")


for message in test_string.split("\n"):
	matches = dewey_validator.findall(message)
	for match in matches:
		print(match[0])
	if len(matches) > 0:
		print("-----------")
