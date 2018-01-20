import argparse

argp = argparse.ArgumentParser()
argp.add_argument('sonnet_input')
args = argp.parse_args()

lines = [x.strip() for x in open(args.sonnet_input)]
buffer = []
for line in lines:
  line = line.strip()
  if not line:
    if len(buffer) == 1: # Get rid of sonnet index buffers
      print()
      buffer = []
      continue
    if len(buffer) != 14:
      buffer = []
      print("Irregular sonnet. Skipping...")
      continue
    quatrains = [buffer[0:3],buffer[3:6], buffer[6:9], buffer[9:11]]
    for quatrain in quatrains:
      quatrain_line = ' EOS '.join(quatrain)
      print(quatrain_line)
    buffer = []
  else:
    buffer.append(line)
