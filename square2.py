"""
PROBLEM: Cash App Boost Recommendation System

Cash App Boosts are instant rewards you can use with your Cash Card
such as "$1 Off Any Coffee Shop" or "10% Off Whole Foods".

To better serve our customers, we would like to recommend relevant Boosts that
they haven't used before. A simple way to do this is: for a customer, find a
group of similar customers and recommend any Boosts the group has used but the
customer hasn't.

You will be provided customer / Boost usage data so that you can construct
customer profile vectors. To determine customer similarity, you will compare
customer profile vectors using the cosine similarity metric (which is provided
for you). Finally, for a given customer, you will provide a list of Boost
recommendations that the customer has never used before with new Boosts from
more similar customers coming first.

INPUT:
- boost_matrix: List[List[int]] - Customer Boost matrix where every row
  represents a customer, every column represents a Boost, and every cell
  represents if the customer has used that Boost before (1 = used, 0 = not used)
- boost_descriptions: Dict[int, str] - Dictionary mapping boost_id to description
- target_customer_idx: int - The index of the customer we want recommendations for
- k: int - Number of similar customers to consider

OUTPUT:
- List[str] - List of Boost descriptions recommended for the target customer,
  ordered by relevance (boosts used by more similar customers first)

EXAMPLE:
If k=3 and the 3 most similar customers to customer 0 are:
- Customer 5 used boosts [1, 3, 4]
- Customer 2 used boosts [1, 2, 5]
- Customer 8 used boosts [1, 4]

And customer 0 has already used boost 1, then recommend:
- Boost 4 (used by 2 similar customers)
- Boost 3 (used by 1 similar customer)
- Boost 2 (used by 1 similar customer)
- Boost 5 (used by 1 similar customer)
"""

from typing import Dict, List
import scipy.spatial.distance

def cosine_similarity(vector1, vector2):
    """Calculate cosine similarity between two vectors"""
    return 1 - scipy.spatial.distance.cosine(vector1, vector2)

# Boost indexes and their associated descriptions
boost_descriptions = {
    0: "10% Off McDonald's",
    1: "$1 Off Any Pizza Shop",
    2: "$1 Off Any Coffee Shop",
    3: "10% Off Chipotle",
    4: "10% Off Whole Foods",
    5: "$2 Off Twitch",
}

# Customer Boost matrix where every row represents a customer,
# every column represents a Boost, and every cell represents
# if the customer has used that Boost before.

# Ex: 10 Customers, 6 Boosts Each ... see above
customer_boost_matrix = [
    [1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0],
]

# Example output using k=3 similar customers for customer 0
# Expected: ['$1 Off Any Coffee Shop', '10% Off Whole Foods', '10% Off Chipotle']


def boost_recommendation_based_on_k_similar_customers(boost_matrix: List[List[int]], boost_descriptions: Dict[int, str],
    target_customer_idx: int, k: int) -> List[str]:
    """
    Generate boost recommendations for a target customer based on
    k most similar customers.

    Returns: List of boost descriptions ordered by relevance
    """
    # List of Values
    customer = boost_matrix[target_customer_idx]

    # List of Boosts
    customer_boosts = []
    for i in range(0, len(customer)):
        if customer[i]:
            customer_boosts.append(boost_descriptions[i])

    # Look for each row and compute similarty cosine
    similarities = []
    for i in range(0, len(boost_matrix)):
        if i != target_customer_idx:
            similarities.append((cosine_similarity(boost_matrix[i], boost_matrix[target_customer_idx]), i))

    # Sort by similarity
    similarities.sort(reverse=True)
    print(similarities[:k])
    # Calculate the k most similar indicies
    k_most_similar = similarities[:k]

    # Compile Recommendations
    recomendations = []
    print(recomendations)
    for _, similar_customer_idx in k_most_similar:
        similar_customer = boost_matrix[similar_customer_idx]
        print(f"Customer: {customer}")
        print(f"Similar Customer: {similar_customer}")

        for i in range(0, len(similar_customer)):
            # Check if there is a boost used by the other customer, but not ours
            if similar_customer[i] and not customer[i]:
                # Only append a new boost
                if boost_descriptions[i] not in recomendations:
                    recomendations.append(boost_descriptions[i])
                    print(f"New Recommendation: {boost_descriptions[i]}")

    return recomendations


    # difference = [bool(customer[idx])^bool(similar_customer[idx]) for idx in range(0, len(customer))]
    # recomendations = [bool(recomendations[idx]) or bool(difference[idx]) for idx in range(0, len(customer))]
    # print(f"Difference: {difference}")
    # print(f"Recomendations: {recomendations}")











# Test your solution
if __name__ == "__main__":
    result = boost_recommendation_based_on_k_similar_customers(customer_boost_matrix, boost_descriptions,
                                                               target_customer_idx=0, k=3)
    print("Recommendations for customer 0:")
    print(result)