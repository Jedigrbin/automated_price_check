# =========================  
# LOAD NEW PRICES  
# =========================  
  
new_prices = {}  
  
with open("new_prices.txt") as f:  
    for line in f:  
        parts = line.strip().split("\t")  
  
        if len(parts) == 2:  
            code, new_price = parts  
            new_prices[code.strip()] = new_price.strip()  
  
# =========================  
# MERGE WITH PRODUCTS FILE  
# =========================  
  
with open("products.txt") as f, \
     open("results.txt", "w") as out, \
     open("changed_items.txt", "w") as changed_out:
  
    # headers  
    header = "CODE\tNAME\tOLD_PRICE\tNEW_PRICE\tCHANGE\n"  
  
    out.write(header)  
    changed_out.write(header)  
  
    for line in f:  
        parts = line.strip().split("\t")  
  
        if len(parts) == 3:  
            code, name, old_price = parts  
  
            code = code.strip()  
            name = name.strip()  
            old_price = old_price.strip()  
  
            # match using code  
            new_price = new_prices.get(code, "NOT_FOUND")  
  
            # compare prices  
            change = "N" if old_price == new_price else "Y"  
  
            # final output line  
            line_out = f"{code}\t{name}\t{old_price}\t{new_price}\t{change}\n"  
  
            # write all items  
            out.write(line_out)  
  
            # write only changed items  
            if change == "Y":  
                changed_out.write(line_out)  
  
print("Done ✔ results.txt and changed_items.txt created")  
