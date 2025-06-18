import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bill Splitter - Interactive", layout="wide")

def calculate_bill_split(people, items, prices, quantities, weights):
    """
    Calculate bill split based on the same logic as the Excel formulas
    """
    # Calculate final prices for each item
    final_prices = [price * qty for price, qty in zip(prices, quantities)]
    
    # Calculate weighted splits for each person-item combination
    splits = {}
    for person_idx, person in enumerate(people):
        splits[person] = []
        for item_idx, item in enumerate(items):
            if len(weights) > item_idx and len(weights[item_idx]) > person_idx:
                weight = weights[item_idx][person_idx]
                # Sum of all weights for this item
                total_weight = sum(weights[item_idx]) if weights[item_idx] else 0
                
                # Weighted split formula: (weight/total_weight) * final_price
                if total_weight > 0:
                    split_amount = (weight / total_weight) * final_prices[item_idx]
                else:
                    split_amount = 0
            else:
                split_amount = 0
            splits[person].append(split_amount)
    
    return final_prices, splits

def main():
    st.title("🧾 Interactive Bill Splitter")
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 People")
        people_input = st.text_area(
            "Enter names (comma-separated)", 
            "Adam, Bob, Charlie, David",
            height=100
        )
        people = [p.strip() for p in people_input.split(",") if p.strip()]
    
    with col2:
        st.subheader("🛒 Items")
        items_input = st.text_area(
            "Enter items (comma-separated)", 
            "Food, Drinks, Tax, Tips",
            height=100
        )
        items = [i.strip() for i in items_input.split(",") if i.strip()]
    
    if people and items:
        st.markdown("---")
        
        # Price and Quantity Input Section
        st.subheader("💰 Item Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Items**")
            for item in items:
                st.write(f"• {item}")
        
        with col2:
            st.write("**Prices (₹)**")
            prices = []
            for i, item in enumerate(items):
                price = st.number_input(
                    f"{item} (₹)", 
                    min_value=0, 
                    value=0, 
                    step=1,
                    key=f"price_{i}"
                )
                prices.append(price)
        
        with col3:
            st.write("**Qty**")
            quantities = []
            for i, item in enumerate(items):
                qty = st.number_input(
                    f"{item}", 
                    min_value=0, 
                    value=1,
                    key=f"qty_{i}",
                    help=f"Quantity for {item}"
                )
                quantities.append(qty)
        
        # Calculate final prices
        final_prices = [price * qty for price, qty in zip(prices, quantities)]
        total_bill = sum(final_prices)
        
        # Display final prices
        st.markdown("---")
        st.subheader("📊 Final Prices")
        
        final_price_data = {
            "Item": items,
            "Price": [f"₹{p}" for p in prices],
            "Quantity": quantities,
            "Final Price": [f"₹{fp}" for fp in final_prices]
        }
        
        st.dataframe(pd.DataFrame(final_price_data), use_container_width=True)
        st.metric("**Total Bill**", f"₹{total_bill}")
        
        # Weight Input Section (like the second table in Excel)
        st.markdown("---")
        st.subheader("⚖️ Weight Assignment")
        st.write("Assign weights to determine how much each person consumed of each item. For equal sharing, use the same number for all people.")
        
        weights = []
        for item_idx, item in enumerate(items):
            st.write(f"**{item}** (Final Price: ₹{final_prices[item_idx]})")
            
            cols = st.columns(len(people))
            item_weights = []
            
            for person_idx, person in enumerate(people):
                with cols[person_idx]:
                    weight = st.number_input(
                        f"{person}",
                        min_value=0,
                        value=0,
                        step=1,
                        key=f"weight_{item_idx}_{person_idx}",
                        help=f"Weight for {person}"
                    )
                    item_weights.append(weight)
            
            weights.append(item_weights)
            
            # Show weight totals and validation
            total_weight = sum(item_weights)
            if total_weight > 0:
                st.success(f"Total weight: {total_weight}")
            else:
                st.warning("No weights assigned for this item")
        
        # Calculate splits
        if any(sum(w) > 0 for w in weights):
            st.markdown("---")
            st.subheader("💸 Bill Split Results")
            
            # Calculate individual splits
            splits = {}
            for person_idx, person in enumerate(people):
                splits[person] = []
                for item_idx, item in enumerate(items):
                    weight = weights[item_idx][person_idx]
                    total_weight = sum(weights[item_idx])
                    
                    if total_weight > 0:
                        split_amount = (weight / total_weight) * final_prices[item_idx]
                    else:
                        split_amount = 0
                    splits[person].append(split_amount)
            
            # Create split table
            split_data = {"Person": people}
            for item_idx, item in enumerate(items):
                split_data[item] = [f"₹{splits[person][item_idx]:.0f}" for person in people]
            
            # Add person totals
            person_totals = [sum(splits[person]) for person in people]
            split_data["Total Split"] = [f"₹{total:.0f}" for total in person_totals]
            
            st.dataframe(pd.DataFrame(split_data), use_container_width=True)
            
            # Item totals and balance check
            st.markdown("---")
            st.subheader("✅ Validation & Balance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Item Totals (from splits)**")
                for item_idx, item in enumerate(items):
                    item_total = sum(splits[person][item_idx] for person in people)
                    balance = final_prices[item_idx] - item_total
                    
                    if abs(balance) < 1:  # Considering integer precision
                        st.success(f"{item}: ₹{item_total:.0f} ✅")
                    else:
                        st.error(f"{item}: ₹{item_total:.0f} (Balance: ₹{balance:.0f}) ❌")
            
            with col2:
                st.write("**Summary**")
                total_split = sum(person_totals)
                overall_balance = total_bill - total_split
                
                if abs(overall_balance) < 1:
                    st.success(f"Total Split: ₹{total_split:.0f} ✅")
                    st.success("All amounts properly allocated!")
                else:
                    st.error(f"Total Split: ₹{total_split:.0f}")
                    st.error(f"Balance: ₹{overall_balance:.0f} ❌")
            
            # Payment tracking section
            st.markdown("---")
            st.subheader("💳 Payment Tracking")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Who Paid What?**")
                paid_amounts = []
                for person_idx, person in enumerate(people):
                    paid = st.number_input(
                        f"{person} paid (₹):",
                        min_value=0,
                        value=0,
                        step=1,
                        key=f"paid_{person_idx}"
                    )
                    paid_amounts.append(paid)
            
            with col2:
                st.write("**Final Settlement**")
                settlement_data = {
                    "Person": people,
                    "Paid": [f"₹{paid:.0f}" for paid in paid_amounts],
                    "Should Pay": [f"₹{total:.0f}" for total in person_totals],
                    "Owes (+) / Gets (-)" : [f"₹{paid - total:.0f}" for paid, total in zip(paid_amounts, person_totals)]
                }
                
                st.dataframe(pd.DataFrame(settlement_data), use_container_width=True)
                
                # Summary
                total_paid = sum(paid_amounts)
                if abs(total_paid - total_bill) < 1:
                    st.success(f"✅ Payment verified: ₹{total_paid:.0f}")
                else:
                    st.warning(f"⚠️ Payment mismatch: Paid ₹{total_paid:.0f}, Bill ₹{total_bill:.0f}")

if __name__ == "__main__":
    main()
