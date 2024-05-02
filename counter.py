import json

with open('friends.json', 'r') as file:
    friends = json.load(file)["friends"]

opts = []

for friend in friends:
    for attr in friend['attributes']:
        if not attr['bio'].startswith('x'):
            opts.append(attr)

# get the number of opts that have an attribute of 'image_url'
image_opts = [opt for opt in opts if opt.get('image_url', None)]

# get the number of opts that have an attribute of 'create_image_prompt'
create_image_opts = [opt for opt in opts if opt.get('create_image_prompt', None)]

print(f"Total number of attributes: {len(opts)}")
print(f"Number of attributes with an image_url: {len(image_opts)}")
print(f"Number of attributes with a create_image_prompt: {len(create_image_opts)}")
print(f"Total number of attributes with an image: {len(image_opts) + len(create_image_opts)}")