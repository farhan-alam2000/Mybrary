def addFuzzy(keyword, d):
  # Initialize the fuzzy keyword set with the given keyword
  fuzzy_keywords = {keyword}
 
  # If the edit distance is greater than 0, generate the fuzzy keyword set for a distance of d-1
  if d > 0:
    prev_keywords = addFuzzy(keyword, d-1)
 
    # For each keyword in the previous set, generate new keywords by inserting or replacing characters
    for prev_keyword in prev_keywords:
      for i in range(len(prev_keyword)+1):
        # Insert a ? character at position i
        new_keyword = prev_keyword[:i] + "?" + prev_keyword[i:]
        fuzzy_keywords.add(new_keyword)
 
        # Replace the i-th character with a ? character
        if i < len(prev_keyword):
          new_keyword = prev_keyword[:i] + "?" + prev_keyword[i+1:]
          fuzzy_keywords.add(new_keyword)
 
  # Return the generated fuzzy keyword set
  return fuzzy_keywords