import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bill Splitter - Interactive", layout="wide")

def calculate_bill_split(people, items, final_prices, weights):
    """
    Calculate bill split based on weighted distribution
    """
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
    
    return splits

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
    
    # Single comprehensive matrix approach
    st.subheader("📊 Bill Split Matrix")
    st.info("💡 **Instructions**: Edit the matrix directly - add items, prices, and weights for each person!")
    
    # Add control for number of people
    num_people = st.number_input("� Number of People", min_value=1, max_value=20, value=4, step=1,
                                help="How many people are splitting the bill?")
    
    # Get people names
    st.write("**👥 Enter People Names:**")
    people_cols = st.columns(min(num_people, 4))  # Max 4 columns for better layout
    people_names = []
    
    for i in range(num_people):
        col_idx = i % 4
        with people_cols[col_idx]:
            if i < 4:
                default_names = ["Alice", "Bob", "Charlie", "Diana"]
                default = default_names[i] if i < len(default_names) else f"Person {i+1}"
            else:
                default = f"Person {i+1}"
            
            person_name = st.text_input(f"Person {i+1}", value=default, key=f"person_{i}")
            people_names.append(person_name)
    
    # Add instructions
    with st.expander("📖 How to Use the Matrix"):
        st.markdown("""
        **Matrix Layout (Rows = Items, Columns = People):**
        - **Column 1**: Enter item names (Pizza, Drinks, etc.)
        - **Column 2**: Enter item prices (₹800, ₹200, etc.)
        - **Remaining Columns**: Enter weights for each person (0 = doesn't pay, 1 = normal share, 2+ = larger share)
        
        **How to Edit:**
        1. Add item names in the first column
        2. Add corresponding prices in the second column
        3. For each item, enter weights for each person in their respective columns
        4. Use the + button to add more items (rows are dynamic)
        5. All calculations update automatically
        
        **💡 Tip**: This layout makes it easy to see each person's involvement in every item!
        """)
    
    # Create matrix with rows=items, columns=people
    initial_data = {
        'Item': ['', '', '', ''],  # Start with 4 empty item rows
        'Price (₹)': ['', '', '', '']  # Corresponding price column
    }
    
    # Add columns for each person
    for i, person_name in enumerate(people_names):
        initial_data[person_name] = ['', '', '', '']  # Start with 4 empty rows for each person
    
    matrix_df = pd.DataFrame(initial_data)
    
    # Configure column types with detailed placeholders
    column_config = {
        "Item": st.column_config.TextColumn(
            "Item", 
            help="Enter item names (e.g., Pizza, Drinks, Dessert, Delivery)"
        ),        "Price (₹)": st.column_config.NumberColumn(
            "Price (₹)", 
            help="Enter item prices (e.g., 800, 200, 150, 50)",
            min_value=0,
            step=1,
            format="%.0f"  # Display as whole numbers
        )
    }
    
    # Configure columns for each person
    for person_name in people_names:
        column_config[person_name] = st.column_config.NumberColumn(
            person_name, 
            help=f"Enter {person_name}'s weight for each item (0 = doesn't pay, 1 = normal share, 2+ = larger share)",
            min_value=0,
            step=1,
            format="%.0f"  # Display as whole numbers
        )
    
    # Use data_editor for the comprehensive matrix with clear placeholder guidance
    st.markdown("**💡 Placeholder Examples:**")
    st.markdown("• **Item Column:** Pizza, Drinks, Dessert, Delivery, etc.")
    st.markdown("• **Price Column:** 800, 200, 150, 50, etc.")  
    st.markdown(f"• **People Columns:** {', '.join(people_names[:3])}{'...' if len(people_names) > 3 else ''}")
    st.markdown("• **Weights:** 0 = doesn't pay, 1 = normal share, 2 = double share, 3 = triple share")
    st.markdown(f"**📊 Current Matrix:** {num_people} people × items (add rows as needed)")
    
    edited_matrix = st.data_editor(
        matrix_df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",  # Allow adding/removing rows (items)
        key=f"main_matrix_people_{num_people}"  # Unique key for different number of people
    )
    
    # Process the matrix to extract data (new format: rows=items, columns=people)
    if not edited_matrix.empty and len(edited_matrix) >= 1:
        # Extract items and prices from each row
        items = []
        final_prices = []
        
        for idx, row in edited_matrix.iterrows():
            item_name = str(row['Item']).strip()
            if item_name and item_name.lower() != 'nan':  # Only include non-empty items
                items.append(item_name)
                
                # Extract price
                try:
                    price = float(row['Price (₹)']) if pd.notna(row['Price (₹)']) and row['Price (₹)'] != '' else 0
                    final_prices.append(max(0, price))  # Ensure non-negative
                except:
                    final_prices.append(0)
        
        # Extract people names and weights
        people = people_names  # Use the names entered by user
        weights = []
        
        # For each item, get weights for all people
        for idx, row in edited_matrix.iterrows():
            item_name = str(row['Item']).strip()
            if item_name and item_name.lower() != 'nan':  # Only process rows with valid items
                item_weights = []
                for person_name in people_names:
                    try:
                        weight = float(row[person_name]) if pd.notna(row[person_name]) and row[person_name] != '' else 0
                        item_weights.append(max(0, weight))  # Ensure non-negative
                    except:
                        item_weights.append(0)
                weights.append(item_weights)
        
        # Display summary
        if items and people:
            total_bill = sum(final_prices)
            
            st.markdown("---")
            st.subheader("📋 Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 People", len(people))
            with col2:
                st.metric("🛒 Items", len(items))
            with col3:
                st.metric("🧾 Total Bill", f"₹{total_bill}")
              # Show extracted data for verification
            if st.checkbox("🔍 Show Extracted Data (for verification)"):
                st.write("**Items & Prices:**")
                for item, price in zip(items, final_prices):
                    st.write(f"• {item}: ₹{price}")
                
                st.write("**People:**")
                st.write(f"• {', '.join(people)}")
        
        # Calculate splits if we have valid data
        if items and people and any(sum(w) > 0 for w in weights):
            # Calculate individual splits using the optimized function
            splits = calculate_bill_split(people, items, final_prices, weights)
            
            st.markdown("---")
            st.subheader("💸 Bill Split Results")
            
            # Create main split table
            split_data = {"Person": people}
            for item_idx, item in enumerate(items):
                split_data[item] = [f"₹{splits[person][item_idx]:.0f}" for person in people]
            
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
            total_bill = sum(final_prices)
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
                hide_index=True
            )
            
            # Extract paid_amounts
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
            st.subheader("🔄 Settlement Transactions")
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
                
                # WhatsApp Summary Section
                st.markdown("---")
                st.subheader("📱 WhatsApp Summary")
                st.info("💬 **Copy & paste this summary to share with your friends on WhatsApp**")
                
                # Generate WhatsApp-friendly text summary
                whatsapp_summary = generate_whatsapp_summary(
                    items, final_prices, people, person_totals, 
                    paid_amounts, transactions, total_bill
                )
                
                # Display the summary in a text area for easy copying
                st.text_area(
                    "📋 Copy this text and send it on WhatsApp:",
                    value=whatsapp_summary,
                    height=400,
                    help="Click inside the box and use Ctrl+A to select all, then Ctrl+C to copy"
                )
                
                # Detailed Export Section
                st.markdown("---")
                st.subheader("💾 Export Detailed Summary")
                st.info("📁 **Save a comprehensive record of this bill split for your reference**")
                
                # Create weight matrix for export (reconstruct from extracted data)
                export_weights = pd.DataFrame({
                    'Person': people,
                    **{item: weights[i] for i, item in enumerate(items)}
                })
                
                # Generate detailed export content
                detailed_summary = generate_detailed_export(
                    items, final_prices, people, person_totals, paid_amounts, 
                    transactions, total_bill, export_weights, weights
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Text file download
                    st.download_button(
                        label="📄 Download as Text File",
                        data=detailed_summary,
                        file_name=f"bill_split_summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        help="Download a detailed text file with all bill split information"
                    )
                
                with col2:
                    # CSV export button
                    csv_data = generate_csv_export(items, final_prices, people, person_totals, paid_amounts, export_weights)
                    st.download_button(
                        label="📊 Download as Excel/CSV",
                        data=csv_data,
                        file_name=f"bill_split_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Download bill data in spreadsheet format for analysis"
                    )
                  # Preview of detailed summary
                with st.expander("🔍 Preview Detailed Summary"):
                    st.text_area("Preview of the detailed export file:", value=detailed_summary, height=300, disabled=True)

def generate_whatsapp_summary(items, final_prices, people, person_totals, paid_amounts, transactions, total_bill):
    """
    Generate a WhatsApp-friendly text summary of the bill split
    """
    summary = "💰 **BILL SPLIT SUMMARY** 💰\n"
    summary += "=" * 30 + "\n\n"
    
    # Bill breakdown
    summary += "🧾 **BILL BREAKDOWN:**\n"
    for i, (item, price) in enumerate(zip(items, final_prices)):
        summary += f"• {item}: ₹{price:.0f}\n"
    summary += f"\n💸 **TOTAL BILL: ₹{total_bill:.0f}**\n\n"
    
    # Individual shares
    summary += "👥 **INDIVIDUAL SHARES:**\n"
    for i, (person, total) in enumerate(zip(people, person_totals)):
        paid = paid_amounts[i]
        balance = paid - total
        status = "✅ Settled" if abs(balance) < 1 else f"{'💰 Owes' if balance < 0 else '💸 Gets back'} ₹{abs(balance):.0f}"
        summary += f"• {person}: Should pay ₹{total:.0f} | Paid ₹{paid:.0f} | {status}\n"
    
    # Settlement transactions
    if transactions:
        summary += f"\n💳 **SETTLEMENT NEEDED:**\n"
        for from_person, to_person, amount in transactions:
            summary += f"• {from_person} → {to_person}: ₹{amount:.0f}\n"
        summary += "\n📝 **Complete the above transactions to settle the bill!**\n"
    else:
        summary += f"\n🎉 **ALL SETTLED!** No transactions needed.\n"
    
    # Footer
    summary += f"\n" + "=" * 30 + "\n"
    summary += "Generated by Bill Splitter App 🧾\n"
    summary += f"📅 {pd.Timestamp.now().strftime('%d %b %Y, %I:%M %p')}"
    
    return summary

def generate_detailed_export(items, final_prices, people, person_totals, paid_amounts, transactions, total_bill, edited_weights, weights):
    """
    Generate a comprehensive detailed export of the bill split
    """
    timestamp = pd.Timestamp.now().strftime('%d %B %Y, %I:%M %p')
    
    summary = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           DETAILED BILL SPLIT SUMMARY                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📅 Generated: {timestamp}
🧾 Total Bill Amount: ₹{total_bill:.2f}
👥 Number of People: {len(people)}
🛒 Number of Items: {len(items)}

═══════════════════════════════════════════════════════════════════════════════
                                  PARTICIPANTS
═══════════════════════════════════════════════════════════════════════════════
{', '.join(people)}

═══════════════════════════════════════════════════════════════════════════════
                                 BILL BREAKDOWN
═══════════════════════════════════════════════════════════════════════════════
"""
    
    for i, (item, price) in enumerate(zip(items, final_prices)):
        summary += f"{i+1:2d}. {item:<30} ₹{price:>8.2f}\n"
    
    summary += f"\n{'Total Bill Amount:':<32} ₹{total_bill:>8.2f}\n"
    
    # Weight Matrix
    summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                               WEIGHT ASSIGNMENT MATRIX
═══════════════════════════════════════════════════════════════════════════════
"""
    
    # Header for weight matrix
    header = f"{'Person':<15}"
    for item in items:
        header += f"{item[:10]:<12}"
    summary += header + "\n" + "─" * len(header) + "\n"
    
    # Weight matrix rows
    for person_idx, person in enumerate(people):
        row = f"{person:<15}"
        for item in items:
            weight = edited_weights.loc[person_idx, item]
            row += f"{weight:<12}"
        summary += row + "\n"
    
    # Weight totals
    summary += "─" * len(header) + "\n"
    totals_row = f"{'TOTALS:':<15}"
    for item in items:
        total_weight = sum(edited_weights[item])
        totals_row += f"{total_weight:<12}"
    summary += totals_row + "\n"
    
    # Individual Split Details
    summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                              INDIVIDUAL SPLIT BREAKDOWN
═══════════════════════════════════════════════════════════════════════════════
"""
    
    for person_idx, person in enumerate(people):
        summary += f"\n🧑 {person.upper()}:\n"
        summary += "─" * 50 + "\n"
        person_total = 0
        
        for item_idx, item in enumerate(items):
            weight = weights[item_idx][person_idx]
            total_weight = sum(weights[item_idx])
            if total_weight > 0:
                split_amount = (weight / total_weight) * final_prices[item_idx]
            else:
                split_amount = 0
            person_total += split_amount
            
            if weight > 0:
                percentage = (weight / total_weight * 100) if total_weight > 0 else 0
                summary += f"  {item:<25} Weight: {weight:<3} ({percentage:5.1f}%) → ₹{split_amount:>7.2f}\n"
        
        summary += "─" * 50 + "\n"
        summary += f"  {'TOTAL FOR ' + person.upper():<35} → ₹{person_total:>7.2f}\n"
    
    # Payment Summary
    summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                                PAYMENT SUMMARY
═══════════════════════════════════════════════════════════════════════════════
"""
    
    summary += f"{'Person':<15} {'Should Pay':<12} {'Actually Paid':<15} {'Balance':<12} {'Status'}\n"
    summary += "─" * 75 + "\n"
    
    for i, person in enumerate(people):
        should_pay = person_totals[i]
        paid = paid_amounts[i]
        balance = paid - should_pay
        
        if abs(balance) < 0.01:
            status = "✅ SETTLED"
        elif balance < 0:
            status = f"💰 OWES ₹{abs(balance):.2f}"
        else:
            status = f"💸 GETS ₹{balance:.2f}"
        
        summary += f"{person:<15} ₹{should_pay:<11.2f} ₹{paid:<14.2f} ₹{balance:<11.2f} {status}\n"
    
    # Settlement Transactions
    if transactions:
        summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                              SETTLEMENT TRANSACTIONS
═══════════════════════════════════════════════════════════════════════════════
💡 Complete these transactions to settle all balances:

"""
        for i, (from_person, to_person, amount) in enumerate(transactions):
            summary += f"{i+1}. {from_person} → {to_person}: ₹{amount:.2f}\n"
    else:
        summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                              SETTLEMENT TRANSACTIONS
═══════════════════════════════════════════════════════════════════════════════
🎉 NO TRANSACTIONS NEEDED - ALL BALANCES ARE SETTLED!
"""
    
    summary += f"""
═══════════════════════════════════════════════════════════════════════════════
                                   SUMMARY
═══════════════════════════════════════════════════════════════════════════════
Total Bill Amount:     ₹{total_bill:.2f}
Total Amount Split:    ₹{sum(person_totals):.2f}
Total Amount Paid:     ₹{sum(paid_amounts):.2f}
Balance Verification:  {'✅ VERIFIED' if abs(total_bill - sum(person_totals)) < 0.01 else '❌ MISMATCH'}
Payment Verification:  {'✅ VERIFIED' if abs(sum(paid_amounts) - total_bill) < 0.01 else '❌ MISMATCH'}

═══════════════════════════════════════════════════════════════════════════════
Generated by Interactive Bill Splitter
📅 {timestamp}
═══════════════════════════════════════════════════════════════════════════════
"""
    
    return summary

def generate_csv_export(items, final_prices, people, person_totals, paid_amounts, edited_weights):
    """
    Generate CSV data for spreadsheet export
    """
    import io
    
    output = io.StringIO()
    
    # Write basic info
    output.write("Bill Split Summary\n")
    output.write(f"Generated,{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write(f"Total Bill,₹{sum(final_prices):.2f}\n")
    output.write("\n")
    
    # Write items breakdown
    output.write("Items Breakdown\n")
    output.write("Item,Price\n")
    for item, price in zip(items, final_prices):
        output.write(f"{item},₹{price:.2f}\n")
    output.write("\n")
    
    # Write weight matrix
    output.write("Weight Matrix\n")
    header = "Person," + ",".join(items) + "\n"
    output.write(header)
    
    for person_idx, person in enumerate(people):
        row = f"{person},"
        for item in items:
            weight = edited_weights.loc[person_idx, item]
            row += f"{weight},"
        output.write(row.rstrip(',') + "\n")
    output.write("\n")
    
    # Write final amounts
    output.write("Final Split\n")
    output.write("Person,Should Pay,Paid,Balance\n")
    for i, person in enumerate(people):
        should_pay = person_totals[i]
        paid = paid_amounts[i]
        balance = paid - should_pay
        output.write(f"{person},₹{should_pay:.2f},₹{paid:.2f},₹{balance:.2f}\n")
    
    return output.getvalue()

if __name__ == "__main__":
    main()
