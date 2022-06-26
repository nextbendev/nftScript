from IPython.display import display 
from PIL import Image
import random
import json
import os

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    for incomp in config["incompatibilities"]:
      for attr in new_image:
        if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
          return create_new_image(all_images, config)

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount));
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x];
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 1
  for item in all_images:
      item["tokenId"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": config["baseURI"] + "/" + str(token["tokenId"]) + '.png',
        "tokenId": token["tokenId"],
        "name":  config["name"] + str(token["tokenId"]).zfill(pad_amount),
        "description": config["description"],
        "attributes": attributes
    }
    with open('../metadata/' + str(token["tokenId"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('../metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = [];
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("../images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("../images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("../images/" + file_name)
  
  print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "ipfs://{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)

generate_unique_images(100, {
  "layers": [
    {
      "name": "Background",
      "weights": [1, 10, 10, 10, 10, 12, 10, 9, .5, .5, 4, 4, 1, 5, 7, 2, 1],
      "values": ["Blue Splat", "Blue Gradient", "Maroon", "Blue", "Lt Blue", "Off White", "Orange", "Green", "Green Stripe", "Maroon Burst", "Blue Marble", "Green Texture", "Splatter", "Dots", "Brogo", "Studio", "Dream" ],
      "trait_path": "../trait-layers/avaxBackground",
      "filename": ["BGA", "BGB", "BGC", "BGD", "BGE", "BGF", "BGG", "BGH", "BGI", "BGJ", "BGK", "BGL","BGM", "BGN", "BGO", "BGP", "BGQ"  ]
    },
    {
      "name": "Hoodie",
      "values": ["Black", "Pink Gradient", "Green", "Green Peach", "Grey", "Plain", "Space", "Trippy", "White", "Splatter", "desert"],
      "trait_path": "../trait-layers/avaxHoodie",
      "filename": ["Black", "Cymaj", "green", "greenPeach", "grey", "hoodieBase", "space", "Trippy", "white", "yelowsplatter", "desert"],
      "weights": [20, 4, 20, 2, 24, 23, 3, 1, 1, 1, 3]
    },
    {
      "name": "Skin-Tone",
      "values": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
      "trait_path": "../trait-layers/Face",
      "filename": ["almond", "chestnut", "choc", "golden", "honey", "limestone", "porcelain", "tan", "bronze", "paleivory"],
      "weights": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    },
    {
      "name": "Hat",
      "values": ["Black", "Blue", "Cyan", "Green", "Grey", "Pink", "Neon Green", "Majenta", "White"],
      "trait_path": "../trait-layers/Hat",
      "filename": ["black", "blue", "CM", "green", "grey", "hotPink", "Neon Green", "mc", "white"],
      "weights": [22.9, 15, 1, 17, 38, .3, .9, .9, 6.9]
    },
    {
      "name": "Beard",
      "values": ["None", "Brown", "Blonde", "Black", "Grey", "Big Brown", "Big Blonde", "Big Black", "Big Grey", "Moustache", "Goatee"],
      "trait_path": "../trait-layers/Beard",
      "filename": ["None", "Brown", "Blonde", "Black", "Grey", "BrownBeard", "BlondeBeard", "BlackBeard", "greyBeard", "Moustache", "Goatee"],
      "weights": [70.75, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1]
    },
    {
      "name": "Hat Type",
      "values": ["AAVE", "ADA", "AVAX", "BSC", "DOGE", "BTC", "ETH", "LOOKS", "MATIC", "None", "Rare", "SHIB", "SOL", "XTZ", "TRX", "Brogo", "Illuminati"],
      "trait_path": "../trait-layers/HatLogo",
      "filename": ["aave", "ada", "avax", "bsc", "doge", "btc", "eth", "looks", "matic", "none", "RareEth", "shib", "sol", "tezos", "trx", "fullBrogo", "illuminati"],
      "weights": [2, 2, 9, 2.75, 2, 1.75, 3.75, 2, 2, 61.50, 1.5, 2, 2, 2, 1.75, 1.75, 1]
    },
    {
      "name": "Shirt",
      "values": ["Blue", "Flannel", "Green", "Peach", "Grey", "Luxury", "Maroon", "Red", "Space", "Trippy", "White", "Pink Gradient", "desert"],
      "trait_path": "../trait-layers/avaxShirt",
      "filename": ["blue", "flannel", "green", "greenPeach", "grey", "luxury", "maroon", "red", "space", "trippy", "white", "cymaj", "desert"],
      "weights": [10, 10, 10, 2, 30, 1, 10, 9, 2, 2, 1, 6, 7]
    },     
    {
      "name": "Trait A",
      "values": ["All Piercings", "Pierced Ears", "Left Piercing", "Right Piercing", "Nose Piercing", "None", "Gold Tooth", "Gold Grill", "Gem Grill", "AirPods", "Joint", "Vape", "Down Bad", "GM", "Hopium", "Everythings Ok", "Wen Rug?", "Vee"],
      "trait_path": "../trait-layers/Accessories",
      "filename": ["all", "ears", "Left", "right", "nose", "None", "SoloGold", "gold", "gems", "AirPods", "joint", "pax", "downbad", "GM", "hopium", "meme", "wenrug", "vee"],
      "weights": [.5, 4.5, 3, 1, 1.25, 69.75, .5, .5, .5, 3, 4, 2, 2, 2, 2, 2, 2, 1]
    },
    {
      "name": "Trait B",
      "values": ["None", "Hoodie Brogo", "CB Main", "All Piercings", "Pierced Ears", "Left Piercing", "Right Piercing", "Nose Piercing", "Gold Tooth", "Gold Grill", "Gem Grill", "Brogo","Chain" ],
      "trait_path": "../trait-layers/AccessoriesB",
      "filename": ["None", "HoodieB", "MainB", "allB", "earsB", "LeftB", "rightB", "noseB", "SoloGoldB", "goldB", "gemsB", "spaceBrogo","ChainB" ],
      "weights": [63.9, 5.9, 11.9, .5, .75, 3.5, .5,  2, 5.7, .9, .5,  2.9, 2.15 ] 
    }, 
    {
      "name": "Eyes",
      "values": ["Heterochromia", "Blue", "Brown", "Blue Lens", "Cyan Lens", "Gold Lens", "Green Lens", "Pink Lens", "Majenta Lens", "Purple Lens", "Red Lens", "Yellow Lens", "Green", "Aviator's", "Sunglasses", "3D", "Fire", "Blue Fire", "Green Fire", "Green Visor", "Red Visor"],
      "trait_path": "../trait-layers/Eyes",
      "filename": ["Split", "Blue", "Brown", "BlueLens", "Cyan", "Gold", "GreenLens", "HotPink", "Majenta", "Purple", "Red", "Yellow", "Green", "mirrorLens", "Sunglasses", "3D", "Fire", "BlueFire", "GreenFire", "Visor", "RedVisor"],
      "weights": [1.4, 5.9, 29.1, 2.1, 2.9, 5.95, 3.55, 1, 2, 2.85, 3.25, 4, 3.9, .9, 24, .9, .9, .9, .8, .9, .9]
    },
  ],
  "incompatibilities": [
    {
      "layer": "Trait A",
      "value": "joint",
      "incompatable_with": ["Gold Tooth"]
    },
    {
      "layer": "Trait A",
      "value": "joint",
      "incompatable_with": ["Gold Grill"]
    },
    {
      "layer": "Trait A",
      "value": "joint",
      "incompatable_with": ["Gem Grill"]
    },
    {
      "layer": "Trait A",
      "value": "chain",
      "incompatable_with": ["Big Brown"]
    },
    {
      "layer": "Trait A",
      "value": "chain",
      "incompatable_with": ["Big Black"]
    },
    {
      "layer": "Trait A",
      "value": "chain",
      "incompatable_with": ["Big Blonde"]
    },
    {
      "layer": "Trait A",
      "value": "all",
      "incompatable_with": ["All Piercings"]
    },
    {
      "layer": "Trait A",
      "value": "ears",
      "incompatable_with": ["Pierced Ears"]
    },
    {
      "layer": "Trait A",
      "value": "left",
      "incompatable_with": ["Left Piercing"]
    },
    {
      "layer": "Trait A",
      "value": "right",
      "incompatable_with": ["Right Piercing"]
    }

  ],
  "baseURI": "https://cryptobroskis.com/cryptobroskis/avaxMeta",
  "name": "CryptoBroski's #",
  "description": "CryptoBroski's are a generative art project that aims to create a 100% solar powered crypto mining center. Owning a CryptoBroski gives you access to project's LP which will be fed with mining rewards.  www.cryptobroskis.com"
})

#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)