This python script uses pypff from libpff to parse a .pst email file to a conversation style .json file. This json format is extremely useful in LLM training scenarios.

Install and add libpff and the desired .pst file to the folder. This is a required step.

The script offers two main commands. The browse command simply browses all subfolders to show the number of messages in each. The parse command parses all messages within the root folder (including subfolders) into a .json file.

To run from the command line call parse.py file. The second argument is required and is the .pst file name. The third argument is the above mentioned commands: browse or parse (parse is default). The fourth and any following arguments are the names of email senders who can be classified as assistants in format "first_name last_name". There are no assistants by default.
