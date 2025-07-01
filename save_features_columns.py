import pickle
     feature_columns = [
    'url_length',
    'domain_length',
    'path_length',
    'query_length',
    'num_dots',
    'num_hyphens',
    'num_slashes',
    'num_subdomains',
    'has_at',
    'has_ip',
    'https',
    'has_port_in_url',
    'has_double_slash_redirect',
    'has_suspicious_words'
]

# Save to feature_columns.pkl
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

print("feature_columns.pkl created successfully.")

