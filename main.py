import streamlit as st
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])


# Streamlit app
st.set_page_config(page_title="Chekit", layout="centered")
st.markdown(
    """
    <style>
        header {
            visibility: hidden;
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Chekit - Smart Shopping to Investing 🛍️💹")
st.write("Enter a product name and let AI help you compare shopping vs investing!")

query = st.text_input("Search for a product:")

if st.button("Search"):
    if not query:
        st.error("Please enter a search query.")
    else:
        with st.spinner("Fetching details..."):
            try:
                # Send the query to GPT-4o
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            You are a helpful assistant that provides structured information for displaying in a Streamlit app. For the given product query, return the following details:

                            1. **Product Name**
                            2. **Variations** (e.g., storage capacity or size)
                                a. **Name** (model number or name)
                                b. **Price** (currency symbol and amount CAD/USD/etc.)
                            4. **Product URL** (link to purchase the product)
                            5. **Brand Name**
                            6. **Brand Ticker Symbol**
                            7. **Current Stock Price** (currency symbol and amount)
                            7. **Financial Page URL** (link to the brand's stock page on Google Finance or Yahoo Finance)

                            Provide the response in the following escaped JSON format:
                            
                            {{
                                "product_name": "string",
                                "variations": [
                                    "name":"string",
                                    "price": "string",
                                ]
                                "product_url": "string",
                                "brand_name": "string",
                                "brand_ticker_symbol": "string",
                                "current_stock_price": "string"
                                "financial_page_url": "string"
                            }}

                            Ensure that the values are accurate and concise, and do not include additional text outside of the JSON response.

                            product query = {query}
                            """,
                        }
                    ],
                    model="o1-preview",
                )

                # Parse response
                answer = json.loads(response.choices[0].message.content)
                print(answer["product_name"])
                # Display results
                # st.markdown("### Results")
                # st.write(answer)

                # Parse the JSON response
                try:

                    # Display as a product card
                    st.title("Product Information")

                    # Product details
                    st.subheader(answer["product_name"])
                    for variation in answer["variations"]:
                        st.write(f"\t**{variation["name"]}**: {variation["price"]}")
                        # st.write(f"**Variation:** {variation['name']}")
                        # st.write(f"**Price:** {variation['price']}")
                    st.markdown(f"[**Buy Here**]({answer['product_url']})")

                    # Brand details
                    st.subheader("Brand Information")
                    st.write(f"**Brand Name:** {answer['brand_name']}")
                    st.write(f"**Ticker Symbol:** {answer['brand_ticker_symbol']}")
                    st.write(
                        f"**Current Stock Price:** {answer['current_stock_price']}"
                    )
                    st.markdown(
                        f"[**View Stock Details**]({answer['financial_page_url']})"
                    )

                except json.JSONDecodeError:
                    st.error("Failed to parse the JSON response.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
