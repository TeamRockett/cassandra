from cassandra.solr_service import SolrService
from cassandra.solr_estimator import SolrEstimator

solr = SolrService('cassandra')

print("\n\n\n")
print("Hello! Cassandra is listening to you...")
user_input = input("You: ")

est = SolrEstimator(solr)
while user_input != "Bye":
    res = est.find_best_dialogue(user_input)
    print(res)
    user_input = input("You: ")

print("Cassandra is going to sleep now...")
print("\n\n\n")
