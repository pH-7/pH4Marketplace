import braintree

def braintree_init():
    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        merchant_id="nnrdhv8jcbptkj6z",
        public_key="xjyj3dtj8w3x8kxq",
        private_key="59b5b4248dcd13be8ff29e4f4ade559a"
    )
