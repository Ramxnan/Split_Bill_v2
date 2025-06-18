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

def calculate_settlement_transactions(people, paid_amounts, person_totals):
    """
    Calculate who should pay whom to settle the bill
    Returns a list of transactions: (from_person, to_person, amount)
    """
    # Calculate net amounts (positive = owes money, negative = should receive money)
    net_amounts = {}
    for i, person in enumerate(people):
        net_amounts[person] = person_totals[i] - paid_amounts[i]
    
    # Separate people who owe money from those who should receive money
    debtors = {person: amount for person, amount in net_amounts.items() if amount > 0}
    creditors = {person: -amount for person, amount in net_amounts.items() if amount < 0}
    
    transactions = []
    
    # Sort by amounts to make settling more efficient
    debtors_sorted = sorted(debtors.items(), key=lambda x: x[1], reverse=True)
    creditors_sorted = sorted(creditors.items(), key=lambda x: x[1], reverse=True)
    
    debtor_idx = 0
    creditor_idx = 0
    
    while debtor_idx < len(debtors_sorted) and creditor_idx < len(creditors_sorted):
        debtor_name, debt_amount = debtors_sorted[debtor_idx]
        creditor_name, credit_amount = creditors_sorted[creditor_idx]
        
        # Calculate transaction amount
        transaction_amount = min(debt_amount, credit_amount)
        
        if transaction_amount > 0.01:  # Only include transactions > 1 paisa
            transactions.append((debtor_name, creditor_name, transaction_amount))
        
        # Update amounts
        debtors_sorted[debtor_idx] = (debtor_name, debt_amount - transaction_amount)
        creditors_sorted[creditor_idx] = (creditor_name, credit_amount - transaction_amount)
        
        # Move to next debtor/creditor if current one is settled
        if debtors_sorted[debtor_idx][1] <= 0.01:
            debtor_idx += 1
        if creditors_sorted[creditor_idx][1] <= 0.01:
            creditor_idx += 1
    
    return transactions

def main():
    st.title("🧾 Interactive Bill Splitter")
    st.markdown("*Split bills fairly with weighted distribution*")
    st.markdown("---")
      # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 People")
        people_input = st.text_area(
            "Who's splitting the bill?", 
            placeholder="🧑‍💼 Alice, 👨‍💻 Bob, 👩‍🎨 Carol, 🧑‍🍳 David",
            height=100,
            help="💡 Enter names separated by commas"
        )
        people = [p.strip() for p in people_input.split(",") if p.strip()]
    
    with col2:
        st.subheader("🛒 Items & Categories")
        items_input = st.text_area(
            "What are you splitting?", 
            placeholder="🍕 Food, 🥤 Drinks, 💰 Tax, 🎯 Tips",
            height=100,
            help="💡 Enter items/categories separated by commas"
        )
        items = [i.strip() for i in items_input.split(",") if i.strip()]    
    # Generate Template Button - Show as soon as user starts typing
    if people_input.strip() or items_input.strip():
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Generate Bill Split Template", type="primary", use_container_width=True):
                if not people:
                    st.error("❌ Please enter at least one person's name")
                elif not items:
                    st.error("❌ Please enter at least one item")
                else:
                    st.session_state.show_template = True
                    st.session_state.people = people
                    st.session_state.items = items
                    st.success("✅ Template generated! Scroll down to start splitting the bill.")
                    st.rerun()
      # Show template only after button is clicked and validation passed
    if st.session_state.get('show_template', False):
        # Use session state values to maintain consistency
        people = st.session_state.get('people', people)
        items = st.session_state.get('items', items)
        
        # Add a reset button at the top
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            if st.button("🔄 Reset Template", type="secondary", help="Start over with new people/items"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        st.markdown("---")
          # Price and Quantity Input Section using editable matrix
        st.subheader("💰 Item Details")
        st.info("📝 **Instructions**: Click on cells to edit prices and quantities directly in the table below")
        
        # Create initial dataframe for item details
        item_details_df = pd.DataFrame({
            'Item': items,
            'Price (₹)': [0] * len(items),
            'Quantity': [1] * len(items)
        })
        
        # Use data_editor for Excel-like editing
        edited_item_details = st.data_editor(
            item_details_df,
            column_config={
                "Item": st.column_config.TextColumn("Item", disabled=True),
                "Price (₹)": st.column_config.NumberColumn("Price (₹)", min_value=0, step=1),
                "Quantity": st.column_config.NumberColumn("Quantity", min_value=0, step=1)
            },
            use_container_width=True,
            hide_index=True,
            key="item_details_editor"
        )
        
        # Extract prices and quantities from the edited dataframe
        prices = edited_item_details['Price (₹)'].tolist()
        quantities = edited_item_details['Quantity'].tolist()
        
        # Calculate final prices
        final_prices = [price * qty for price, qty in zip(prices, quantities)]
        total_bill = sum(final_prices)
        
        # Display final prices
        st.markdown("---")
        st.subheader("📊 Final Prices")
        final_price_data = {
            "🍽️ Item": items,
            "💰 Price": [f"₹{p}" for p in prices],
            "🔢 Qty": quantities,
            "💸 Final Price": [f"₹{fp}" for fp in final_prices]
        }
        
        st.dataframe(pd.DataFrame(final_price_data), use_container_width=True, hide_index=True)
        
        # Total bill with better formatting
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.metric("🧾 **Total Bill**", f"₹{total_bill}")
        
        # Weight Input Section using matrix format
        st.markdown("---")
        st.subheader("⚖️ Weight Assignment Matrix")
        st.info("💡 **Tip**: Click cells to edit weights, or use Quick Split buttons below")
        
        # Add instructions for editing
        with st.expander("📖 How to Edit Weights"):
            st.markdown("""
            **Editing Tips:**
            1. **Click on a cell** → Type new number → **Press Enter**
            2. **Weight 0** = Person doesn't pay for this item
            3. **Weight 1** = Normal share
            4. **Weight 2+** = Larger share (e.g., if someone ate more)
            
            **Quick Split Buttons:** Set everyone to equal weight (1) for that item
            """)
          # Create initial weight matrix with session state
        if 'weight_matrix' not in st.session_state or len(st.session_state.weight_matrix) == 0:
            st.session_state.weight_matrix = pd.DataFrame({
                'Person': people,
                **{item: [0] * len(people) for item in items}
            })
        
        # Update matrix if people or items changed
        current_people = set(st.session_state.weight_matrix['Person'])
        current_items = set(st.session_state.weight_matrix.columns[1:])
        if current_people != set(people) or current_items != set(items):
            st.session_state.weight_matrix = pd.DataFrame({
                'Person': people,
                **{item: [0] * len(people) for item in items}
            })
        
        # Create layout for buttons above each item column
        matrix_cols = st.columns([1.2] + [1] * len(items))
        
        # Quick action buttons
        with matrix_cols[0]:
            st.write("**Quick Actions:**")
        
        # Handle button clicks and apply to session state
        for idx, item in enumerate(items):
            with matrix_cols[idx + 1]:
                # Create a more specific button label
                button_key = f"split_{item}_{idx}"
                if st.button(f"⚖️ Split {item[:8]}{'...' if len(item) > 8 else ''}", 
                           key=button_key,
                           help=f"Set equal weights for all people for {item}", 
                           use_container_width=True,
                           type="primary"):
                    # Apply equal split to session state
                    for person_idx in range(len(people)):
                        st.session_state.weight_matrix.loc[person_idx, item] = 1
                    st.rerun()
        
        st.write("")  # Spacing
        
        # Configure columns for the weight matrix editor
        column_config = {
            "Person": st.column_config.TextColumn("Person", disabled=True)
        }
        for item in items:
            column_config[item] = st.column_config.NumberColumn(
                item, 
                min_value=0, 
                step=1,
                help=f"Weight for {item}"
            )
        
        # Use data_editor for matrix input with session state
        edited_weights = st.data_editor(
            st.session_state.weight_matrix,
            column_config=column_config,
            use_container_width=True,
            hide_index=True,
            key="weight_matrix_editor"
        )
        
        # Update session state with edited weights
        st.session_state.weight_matrix = edited_weights
        
        # Convert matrix to the format expected by the calculation function
        weights = []
        for item_idx, item in enumerate(items):
            item_weights = edited_weights[item].tolist()
            weights.append(item_weights)
        
        # Create and display weight totals summary table
        weight_totals_data = {'💭 Summary': ['TOTAL WEIGHTS']}
        for item in items:
            item_weights = edited_weights[item].tolist()
            total_weight = sum(item_weights)
            weight_totals_data[item] = [total_weight]
        
        weight_totals_df = pd.DataFrame(weight_totals_data)
        
        st.write("**📊 Weight Totals:**")
        st.dataframe(weight_totals_df, use_container_width=True, hide_index=True)
        
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
            
            # Create main split table (just the people)
            split_data = {"Person": people}
            for item_idx, item in enumerate(items):                split_data[item] = [f"₹{splits[person][item_idx]:.0f}" for person in people]
            
            # Add person totals
            person_totals = [sum(splits[person]) for person in people]
            split_data["Total Split"] = [f"₹{total:.0f}" for total in person_totals]
            
            split_df = pd.DataFrame(split_data)
            st.dataframe(split_df, use_container_width=True, hide_index=True)
            
            # Create separate summary table for item totals and balance
            st.write("**Split Summary & Validation:**")
            
            # Calculate item totals
            summary_data = {"Summary": ["Item Totals", "Expected (Final Price)", "Balance"]}
            for item_idx, item in enumerate(items):
                item_total = sum(splits[person][item_idx] for person in people)
                balance = final_prices[item_idx] - item_total
                
                summary_data[item] = [
                    f"₹{item_total:.0f}",
                    f"₹{final_prices[item_idx]:.0f}",
                    f"₹{balance:.0f} {'✅' if abs(balance) < 1 else '❌'}"
                ]
            
            # Add total column
            total_split_amount = sum(person_totals)
            overall_balance = total_bill - total_split_amount
            summary_data["Total Split"] = [
                f"₹{total_split_amount:.0f}",
                f"₹{total_bill:.0f}",
                f"₹{overall_balance:.0f} {'✅' if abs(overall_balance) < 1 else '❌'}"
            ]
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            # Quick validation summary
            if abs(overall_balance) < 1:
                st.success("✅ All amounts properly allocated!")
            else:
                st.error("❌ Balance mismatch detected")
              # Payment tracking section
            st.markdown("---")
            st.subheader("💳 Payment Tracking")
            st.info("💡 **Tip**: Enter how much each person actually paid")
            
            # Create payment tracking dataframe
            payment_df = pd.DataFrame({
                '👤 Person': people,
                '💰 Paid (₹)': [0] * len(people)
            })
              # Use data_editor for payment input
            edited_payments = st.data_editor(
                payment_df,
                column_config={
                    "👤 Person": st.column_config.TextColumn("👤 Person", disabled=True),
                    "💰 Paid (₹)": st.column_config.NumberColumn("💰 Paid (₹)", min_value=0, step=1)
                },
                use_container_width=True,
                hide_index=True,
                key="payment_editor"
            )
            
            # Extract paid amounts
            paid_amounts = edited_payments['💰 Paid (₹)'].tolist()
            
            # Display settlement summary
            st.markdown("---")
            st.subheader("📊 Final Settlement Summary")
            settlement_data = {
                "👤 Person": people,
                "💸 Paid": [f"₹{paid:.0f}" for paid in paid_amounts],
                "🎯 Should Pay": [f"₹{total:.0f}" for total in person_totals],
                "⚖️ Balance": [f"₹{paid - total:.0f}" for paid, total in zip(paid_amounts, person_totals)]
            }
            
            st.dataframe(pd.DataFrame(settlement_data), use_container_width=True, hide_index=True)
            
            # Summary
            total_paid = sum(paid_amounts)
            if abs(total_paid - total_bill) < 1:
                st.success(f"✅ Payment verified: ₹{total_paid:.0f}")
            else:
                st.warning(f"⚠️ Payment mismatch: Paid ₹{total_paid:.0f}, Bill ₹{total_bill:.0f}")
              # Settlement transactions
            st.markdown("---")
            st.subheader("� Settlement Transactions")
            st.info("💡 **Who needs to pay whom to settle the bill**")
            
            transactions = calculate_settlement_transactions(people, paid_amounts, person_totals)
            
            if not transactions:
                st.success("🎉 Perfect! No transactions needed - all balances are settled")
            else:
                transaction_df = pd.DataFrame(transactions, columns=["💸 From", "💰 To", "💵 Amount (₹)"])
                # Format the amount column
                transaction_df["💵 Amount (₹)"] = transaction_df["💵 Amount (₹)"].apply(lambda x: f"₹{x:.0f}")
                st.dataframe(transaction_df, use_container_width=True, hide_index=True)
                
                # Instructions for using the transaction table
                with st.expander("📖 How to Use These Transactions"):
                    st.markdown("""
                    **Settlement Guide:**
                    - **💸 From**: Person who owes money and needs to pay
                    - **💰 To**: Person who should receive the money  
                    - **💵 Amount**: Exact amount to transfer
                    
                    **Payment Methods:**
                    - 💳 Digital: UPI, PayTM, Google Pay, etc.
                    - 💵 Cash: Physical money transfer
                    - 🏦 Bank: Direct transfer
                    
                    💡 **Pro Tip**: Complete all transactions shown above to fully settle the bill!
                    """)

if __name__ == "__main__":
    main()
