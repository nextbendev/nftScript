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

generate_unique_images(7777, {
  "layers": [
    {
      "name": "Background",
      "weights": [1, 10, 10, 10, 10, 12, 10, 8.75, .5, .5, 4, 4, 1, 5, 7, 2, 1, .25],
      "values": ["Blue Splat", "Blue Gradient", "Maroon", "Blue", "Lt Blue", "Off White", "Orange", "Green", "Damaged Green", "Maroon Burst", "Blue Marble", "Green Texture", "Splatter", "Dots", "Brogo", "Studio", "Dream", "Black" ],
      "trait_path": "../trait-layers/avaxBackground",
      "filename": ["BGA", "BGB", "BGC", "BGD", "BGE", "BGF", "BGG", "BGH", "BGI", "BGJ", "BGK", "BGL","BGM", "BGN", "BGO", "BGP", "BGQ", "Black"  ]
    },
    {
      "name": "Hoodie",
      "values": ["Black", "Sol", "Green", "Green Peach", "Grey", "Plain", "Space", "Trippy", "White", "Splatter", "Desert"],
      "trait_path": "../trait-layers/avaxHoodie",
      "filename": ["Black", "Cymaj", "green", "greenPeach", "grey", "hoodieBase", "space", "Trippy", "white", "yelowsplatter", "desert"],
      "weights": [20, 4, 20, 2, 24, 23, 3, 1, 1, 1, 3]
    },
    {
      "name": "Skin Tone",
      "values": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Ape", "Android", "White Walker", "Zombie"],
      "trait_path": "../trait-layers/Face",
      "filename": ["almond", "chestnut", "choc", "golden", "honey", "limestone", "porcelain", "tan", "bronze", "paleivory", "Ape", "android", "et", "zombie"],
      "weights": [9.7, 9.7, 9.7, 9.7, 9.7, 9.7, 9.6, 9.6, 9.6, 9.7, .5, 1.05, .95, .7]
    },
    {
      "name": "Hat",
      "values": ["Black", "Blue", "Cyan", "Green", "Grey",  "Neon Green", "Bowler", "White", "Top hat" ],
      "trait_path": "../trait-layers/Hat",
      "filename": ["black", "blue", "CM", "green", "grey",  "NeonGreen", "Bowler", "white", "Tophat"],
      "weights": [19.9, 18, 1, 17, 38,  .9, .9, 6.9, .3]
    },
    {
      "name": "Beard",
      "values": ["None", "Brown", "Blonde", "Black", "Grey", "Big Brown", "Big Blonde", "Big Black", "Big Grey", "Selleck", "Goatee", "Moustachio"],
      "trait_path": "../trait-layers/Beard",
      "filename": ["None", "Brown", "Blonde", "Black", "Grey", "brownBeard", "blondeBeard", "blackBeard", "greyBeard", "Moustache", "Goatee", "moust"],
      "weights": [70.25, 3, 3, 3, 3, 3, 3, 3, 3, 1.7, 1, .05]
    },
   
    {
      "name": "Shirt",
      "values": ["Blue", "Flannel", "Green", "Peach", "Grey", "Luxury", "Maroon", "Red", "Space", "Trippy", "White", "Sol", "Desert"],
      "trait_path": "../trait-layers/avaxShirt",
      "filename": ["blue", "flannel", "green", "greenPeach", "grey", "luxury", "maroon", "red", "space", "trippy", "white", "cymaj", "desert"],
      "weights": [14, 2, 14, 2, 20, 1, 20, 9, 2, 2, 1, 6, 7]
    },     
    {
      "name": "Trait A",
      "values": [ "All Piercings",  "Utility Brogo",  "Pierced Ears", "Gem Gril", "Gold Grill", "Gold Brogo", "Pierced Left", "Brogo", "None", "Vape", "Pierced Right", "Gold Tooth", "St. Harambe"],
      "trait_path": "../trait-layers/Accessories",
      "filename": [ "all", "diamondBrogo", "ears", "gems", "gold", "goldBrogo",  "left", "basicLogo", "none", "pax", "right", "soloGold", "harambe" ],
      "weights": [    1 ,         3,          7,     .5 ,     1.5  ,    1 ,          3,      7.5,       73,      2.25,      1,     2.75,       1]
    },
    {
      "name": "Trait B",
      "values": ["Air Pods",  "Dip", "Down Bad", "Gem Grill", "GM", "Gold Grill",  "Hoodie", "Hopium", "Joint", "Everythings Ok", "None", "Vape", "Gold Tooth", "Vee", "Wen", "Bags", "AVAX Hoodie"],
      "trait_path": "../trait-layers/Accessories",
      "filename": ["airPods",   "dip", "downbad",  "gems", "GM", "gold", "Hoodie", "hopium", "joint",  "meme", "none", "pax", "soloGold", "vee",  "wenrug", "zero", "avaxHoodie"],
      "weights": [    2  ,         1,      1,       .25 ,    2 ,    .5  ,   3.75,      1,        4,      1,      73,     2,       1,       1.5,       2,      1.5,    3 ]
    },
    {
      "name": "Trait C",
      "values": ["AAVE", "ADA", "AVAX", "BSC", "DOGE", "BTC", "ETH", "LOOKS", "MATIC", "None", "Rare ETH", "SHIB", "SOL", "XTZ", "TRX", "Brogo", "Illuminati"],
      "trait_path": "../trait-layers/HatLogo",
      "filename": ["aave", "ada", "avax", "bsc", "doge", "btc", "eth", "looks", "matic", "none", "RareEth", "shib", "sol", "tezos", "trx", "fullBrogo", "illuminati"],
      "weights": [1, 1, 5, 1.75, 2, 1.75, 1.75, 2, 2, 70.50, 1.5, 2, 2, 2, 1.75, 1.85, .9]
    },
    {
      "name": "Eyes",
      "values": ["Heterochromia", "Blue", "Brown", "Blue Lens", "Cyan Lens", "Gold Lens", "Green Lens", "Pink Lens", "Majenta Lens", "Purple Lens", "Red Lens", "Yellow Lens", "Green", "Aviator's", "Sunglasses", "3D", "Laser", "Blue Laser", "Green Laser", "Visor", "Terminator"],
      "trait_path": "../trait-layers/Eyes",
      "filename": ["Split", "Blue", "Brown", "BlueLens", "Cyan", "Gold", "GreenLens", "HotPink", "Majenta", "Purple", "Red", "Yellow", "Green", "mirrorLens", "Sunglasses", "3D", "Fire", "BlueFire", "GreenFire", "visor", "terminate"],
      "weights": [1, 5.9, 28.5, 2.1, 2.9, 5.95, 3.55, 1, 2, 2, 3.25, 4, 3.9, .9, 24.8, .9, 1.9, 1, .8, 2, .85 ]
    }
  ],
  "incompatibilities": [
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["ADA"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["ETH"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["AvAX"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["BSC"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["BTC"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["LOOKS"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["Rare ETH"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["MATIC"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["SHIB"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["SOL"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["XTZ"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["TRX"]
    },
    {
      "layer": "Hat",
       "value": "Top Hat",
      "incompatable_with": ["Yuga"]
    },
    {
      "layer": "Trait B",
       "value": "diamondBrogo",
      "incompatable_with": ["Brogo"]
    },
    {
      "layer": "Trait B",
       "value": "diamondBrogo",
      "incompatable_with": ["Gold Brogo"]
    },
    
    {
      "layer": "Trait A",
       "value": "all",
      "incompatable_with": [" Blue Fire"]
    },
    {
      "layer": "Trait A",
       "value": "ears",
      "incompatable_with": [" Blue Fire"]
    },
    {
      "layer": "Trait A",
       "value": "left",
      "incompatable_with": [" Blue Fire"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["ADA"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["ETH"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["AvAX"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["BSC"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["BTC"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["LOOKS"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["Rare ETH"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["MATIC"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["SHIB"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["SOL"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["XTZ"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["TRX"]
    },
    {
      "layer": "Trait C",
       "value": "bowler",
      "incompatable_with": ["Yuga"]
    },
    {
      "layer": "Trait A",
       "value": "White Walker",
      "incompatable_with": ["Nose"]
    },
    {
      "layer": "Trait A",
       "value": "Android",
      "incompatable_with": ["Nose"]
    },
    {
      "layer": "Trait A",
       "value": "White Walker",
      "incompatable_with": ["All"]
    },
    {
      "layer": "Trait A",
       "value": "Android",
      "incompatable_with": ["All"]
    },
    {
      "layer": "Trait A",
       "value": "Android",
      "incompatable_with": ["Gold Tooth"]
    },
    {
      "layer": "Trait A",
       "value": "Android",
      "incompatable_with": ["Gem Grill"]
    },
    {
      "layer": "Trait A",
       "value": "Android",
      "incompatable_with": ["Gold Grill"]
    },

    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["BrownBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["BlackBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["BlondeBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["GreyBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Big Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Big Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Big Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Big Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Big Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Big Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Big Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Big Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Big Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Big Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Big Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Big Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Big Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Big Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Big Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Big Grey"]
    },

    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["brownBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["blackBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["blondeBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["greyBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["brownBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["blackBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["blondeBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["greyBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["brownBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["blackBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["blondeBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["greyBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["brownBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["blackBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["blondeBeard"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["greyBeard"]
    },


    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "ape",
      "incompatable_with": ["Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "android",
      "incompatable_with": ["Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "et",
      "incompatable_with": ["Grey"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Brown"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Black"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Blonde"]
    },
    {
      "layer": "Skin Tone",
       "value": "zombie",
      "incompatable_with": ["Grey"]
    }
  ],
  "baseURI": "https://cryptobroskis.com/cryptobroskis/avaxImg",
  "name": "CryptoBroski's #",
  "description": "CryptoBroski's are a generative art project that aims to create a 100% solar powered crypto mining center. Owning a CryptoBroski gives you access to project's LP which will be fed with mining rewards.  www.cryptobroskis.com"
})

#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)