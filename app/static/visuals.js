const ingredientIcons = [
 [/peanut butter|almond butter|tahini/,'🥜'],[/cream cheese|cheese|ricotta|mascarpone|feta|gorgonzola/,'🧀'],[/butter|margarine|ghee/,'🧈'],[/eggplant|aubergine/,'🍆'],[/egg|mayonnaise/,'🥚'],[/coconut/,'🥥'],[/milk|cream|yogurt|yoghurt|buttermilk/,'🥛'],
 [/sweet potato|yam/,'🍠'],[/potato/,'🥔'],[/tomato|ketchup|marinara/,'🍅'],[/carrot/,'🥕'],[/onion|shallot|scallion|leek/,'🧅'],[/garlic/,'🧄'],[/broccoli/,'🥦'],[/cucumber|pickle|zucchini/,'🥒'],[/corn|polenta|grits/,'🌽'],[/mushroom|shiitake|portobello|portabella/,'🍄'],[/lettuce|spinach|cabbage|kale|choy|arugula|endive|greens|watercress|celery/,'🥬'],[/pea|edamame|green bean/,'🫛'],[/chili|chile|jalapeno|habanero|cayenne|sriracha|gochujang|pepper flakes/,'🌶️'],[/bell pepper|capsicum|pimiento|pimento/,'🫑'],[/olive/,'🫒'],[/ginger|turmeric/,'🫚'],[/pumpkin|squash/,'🎃'],[/asparagus|artichoke|fennel|bamboo|okra/,'🌱'],[/radish|turnip|beet|parsnip|rutabaga/,'🥕'],
 [/strawberr/,'🍓'],[/blueberr/,'🫐'],[/raspberr|blackberr|cranberr|currant/,'🫐'],[/cherr/,'🍒'],[/banana/,'🍌'],[/pineapple/,'🍍'],[/mango|papaya/,'🥭'],[/avocado/,'🥑'],[/apple/,'🍎'],[/pear/,'🍐'],[/peach|nectarine|apricot/,'🍑'],[/orange|tangerine|mandarin|clementine|grapefruit/,'🍊'],[/lemon|lime/,'🍋'],[/grape|raisin/,'🍇'],[/kiwi/,'🥝'],[/watermelon/,'🍉'],[/melon|cantaloupe/,'🍈'],[/fig|date|plum|prune|fruit/,'🍇'],
 [/chicken|turkey|duck|poultry/,'🍗'],[/bacon/,'🥓'],[/sausage|kielbasa|chorizo|frankfurter|hot dog/,'🌭'],[/beef|steak|veal|lamb|venison/,'🥩'],[/pork|ham|prosciutto|salami|rib/,'🍖'],[/shrimp|prawn/,'🦐'],[/lobster|crayfish|crawfish/,'🦞'],[/crab|surimi/,'🦀'],[/squid|calamari/,'🦑'],[/octopus/,'🐙'],[/clam|oyster|mussel|scallop/,'🦪'],[/salmon|tuna|cod|fish|anchov|sardine|tilapia|trout|halibut/,'🐟'],
 [/rice|quinoa|couscous/,'🍚'],[/pasta|spaghetti|macaroni|penne|linguine|fettuccine|orzo|rotini/,'🍝'],[/noodle|ramen|soba|udon/,'🍜'],[/flour|oat|wheat|barley|bran|semolina|starch|cornmeal|yeast/,'🌾'],[/croissant|crescent/,'🥐'],[/bagel/,'🥯'],[/baguette|french bread/,'🥖'],[/bread|toast|crumb|bun|roll/,'🍞'],[/tortilla|pita|flatbread/,'🫓'],[/wonton|dumpling|gyoza/,'🥟'],[/tofu|tempeh|beans|bean|lentil|chickpea|miso/,'🫘'],[/nuts|nut|almond|pecan|walnut|cashew|pistachio|peanut|hazelnut/,'🥜'],[/chestnut/,'🌰'],[/sesame|seed/,'🌰'],
 [/chocolate|cocoa|nutella/,'🍫'],[/cookie|oreo|cracker|biscuit/,'🍪'],[/cake|frosting|icing/,'🧁'],[/ice cream|sorbet|sherbet/,'🍨'],[/honey|syrup|molasses/,'🍯'],[/sugar|sweetener|splenda|candy|marshmallow|caramel/,'🍬'],[/jam|jelly|preserve/,'🫙'],[/salt|peppercorn|black pepper|white pepper/,'🧂'],[/herb|parsley|basil|mint|cilantro|dill|thyme|oregano|rosemary|sage|tarragon|bay leaf|chive/,'🌿'],[/cinnamon|nutmeg|cumin|paprika|coriander|clove|allspice|spice|seasoning|cardamom/,'🫙'],[/oil|vinegar|sauce|dressing|stock|broth|bouillon|mustard/,'🍶'],[/coffee|espresso|cocoa/,'☕'],[/tea|matcha/,'🍵'],[/wine|sherry|champagne|brandy/,'🍷'],[/beer|ale|stout/,'🍺'],[/rum|vodka|gin|liqueur|whiskey|tequila/,'🍸'],[/juice|soda|lemonade|cola/,'🧃'],[/water/,'💧'],[/ice/,'🧊']
];
function ingredientIcon(id,label){
 const match=ingredientIcons.find(([pattern])=>pattern.test(id.toLowerCase()));
 if(match)return `<span class="ingredient-emoji" aria-hidden="true">${match[1]}</span>`;
 return `<span class="ingredient-jar" aria-hidden="true"><svg viewBox="0 0 60 64"><rect x="13" y="4" width="34" height="8" rx="3" fill="#5e8060"/><rect x="10" y="12" width="40" height="47" rx="10" fill="#edd9ac" stroke="#c4ab78" stroke-width="2"/><rect x="13" y="28" width="34" height="22" rx="3" fill="#fff9e9"/><path d="M17 18v9" stroke="#fff" stroke-width="3" stroke-linecap="round"/><text x="30" y="43" text-anchor="middle" font-size="11" font-weight="bold" fill="#5e8060">${esc(label.slice(0,2))}</text></svg></span>`;
}
const photoRules = [
 [/ice cream|icecream|sorbet|sherbet|snow cone|frozen yogurt/,'icecream'],
 [/smoothie|shake|julius|juice|lemonade|cocktail|drink|sangria|punch|latte/,'smoothie'],
 [/pudding|custard/,'pudding'],[/poached egg|eggs benedict/,'poached'],[/french toast/,'toast'],[/scrambl/,'scramble'],[/omelet|frittata|poached egg|fried egg|eggz|bird nest|egg.*rollup/,'egg'],
 [/nacho|tortilla chip|quesadilla|taco/,'nachos'],[/pizza/,'pizza'],[/wonton|dumpling|gyoza|pierogi|potsticker/,'dumpling'],
 [/cupcake|muffin/,'muffin'],[/pancake|crepe|waffle/,'pancake'],[/cookie|biscuit|shortbread|macaroon/,'cookie'],
 [/truffle|bon bon|bonbon|chocolate ball|fudge|brownie|chocodamia|chocolate delight/,'chocolate'],
 [/cake|torte|tart|pie|cobbler|crumble|crumb bake/,'cake'],
 [/fruit.*salad|grape.*salad|yogurt.*salad|fruit.*topping|fruit.*bowl|yogurt delight/,'fruit'],
 [/salad|coleslaw|slaw/,'salad'],[/creamy.*soup|cream of|bisque|chowder/,'soup'],[/soup|stew|chili con/,'broth'],
 [/casserole|gratin|enchilada|lasagna|lasagne|baked.*cheese/,'casserole'],
 [/pasta|spaghetti|linguine|penne|fettuccine|macaroni|noodle|ravioli|orzo/,'pasta'],
 [/rice|pilaf|risotto|riso/,'rice'],[/sandwich|burger|rollup|wrap/,'sandwich'],
 [/sausage|kielbasa/,'sausage'],[/ribs|riblets/,'ribs'],[/shrimp|prawn|scallop|crab|lobster/,'shrimp'],[/salmon|fish|tuna|cod|tilapia|halibut/,'fish'],
 [/chicken|turkey|duck/,'chicken'],[/beef|steak|pork|lamb|sausage|kielbasa|meatball|meatloaf|ham/,'steak'],
 [/bread|scone|croissant|brioche|bagel|buns|rolls|toast/,'bread'],
 [/dip|salsa|guacamole|chex|cracker|snack/,'nachos']
];
function recipePhoto(recipe){
 const name=recipe.name.toLowerCase();
 const overrides={300627:'chocolate',176131:'nachos',170084:'egg',198142:'fruit',141148:'fruit',382754:'fruit'};
 if(overrides[recipe.id])return {key:overrides[recipe.id],caption:'유사 요리 참고 사진'};
 const direct=photoRules.find(([pattern])=>pattern.test(name));
 if(direct)return {key:direct[1],caption:'유사 요리 참고 사진'};
 const ingredients=(recipe.ingredients||[]).join(' ').toLowerCase();
 const fallback=[[/chocolate|cocoa/,'chocolate'],[/flour.*sugar|sugar.*flour/,'cake'],[/strawberr|banana|mango|pineapple|peach|apple|grape/,'fruit'],[/shrimp|crab|prawn/,'shrimp'],[/salmon|tuna|fish/,'fish'],[/chicken|turkey/,'chicken'],[/beef|pork|sausage|ham|bacon/,'steak'],[/pasta|spaghetti|noodle/,'pasta'],[/rice/,'rice'],[/egg/,'egg'],[/bread/,'bread'],[/potato|cheese/,'casserole'],[/lettuce|spinach|cucumber|vegetable|broccoli/,'salad'],[/milk|yogurt|juice/,'smoothie']].find(([pattern])=>pattern.test(ingredients));
 return {key:fallback?fallback[1]:'casserole',caption:'재료 유형 참고 사진'};
}
