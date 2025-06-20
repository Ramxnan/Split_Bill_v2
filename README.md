# 🧾 Interactive Bill Splitter

A modern, user-friendly Streamlit web application that makes splitting bills among friends, family, or colleagues incredibly easy and fair. No more complicated calculations or awkward conversations about who owes what!

## ✨ Features

### 🎯 **Smart Bill Splitting**
- **Weighted Distribution**: Split items proportionally based on who consumed what
- **Direct Item Entry**: Add items with final prices directly in an intuitive table
- **Manual Weight Control**: Fine-tune weights for complex splitting scenarios
- **Real-time Validation**: Instant feedback on splitting accuracy

### 🎨 **Streamlined User Experience**
- **Three-Step Process**: People → Items → Weights for maximum simplicity
- **Excel-like Interface**: Familiar grid editing with click-to-edit cells
- **Dynamic Tables**: Add/remove rows as needed with flexible editing
- **Visual Feedback**: Color-coded validation (✅ balanced, ❌ mismatch)
- **Mobile Friendly**: Works seamlessly on phones, tablets, and desktops

### 💰 **Complete Financial Tracking**
- **Direct Price Entry**: Enter final prices for each item without separate price/quantity fields
- **Payment Tracking**: Record who actually paid what
- **Settlement Calculator**: Automatic who-owes-whom calculations
- **Transaction Guide**: Step-by-step settlement instructions

### 📱 **Sharing & Export Features**
- **WhatsApp Summary**: Copy-paste ready summary for group chats
- **Detailed Export**: Download comprehensive records as text files
- **CSV Export**: Spreadsheet-compatible data for analysis
- **Complete Documentation**: All weights, calculations, and transactions included

### 🔧 **Smart Features**
- **Zero Session State**: No lag or caching issues - everything loads instantly
- **Auto-calculations**: Real-time totals and splits
- **Balance Validation**: Ensures every rupee is accounted for
- **Weight Summaries**: Clear overview of distribution patterns

## 🚀 How It Works

### **Step 1: 👥 Enter People**
```
Enter names: Alice, Bob, Carol, David
```
- Simple text area input with comma separation
- Instant confirmation of participants added

### **Step 2: 💰 Add Bill Items**
```
Direct table editing:
Item Name          | Final Price (₹)
Food              | 800
Drinks            | 200
Tax & Tips        | 100
```
- Add items with final prices in a dynamic table
- Add or remove rows as needed
- Auto-calculates total bill amount

### **Step 3: ⚖️ Assign Weights**
```
Person  | Food | Drinks | Tax & Tips
Alice   |  1   |   0    |     1
Bob     |  1   |   1    |     1  
Carol   |  1   |   1    |     1
David   |  1   |   0    |     1
```
- Default weights start at 0 (nothing assigned)
- Set weights manually for each person-item combination
- Weight 0 = doesn't pay, Weight 1 = normal share, Weight 2+ = larger share

### **Step 4: 💳 Track Payments & Settle**
- Enter actual payments made by each person
- Get automated settlement calculations
- Download detailed summaries or copy WhatsApp-ready text

## 💡 Example Scenarios

**🍕 Shared Dinner**
- Food: Everyone splits equally (weight 1 each)
- Drinks: Only Alice and Bob had drinks (weight 1 each, others 0)
- Tax & Tips: Split equally among all

**🎉 Group Trip**
- Hotel: Split equally among all travelers
- Meals: Split by who attended each meal
- Activities: Individual choices, individual payments

**🏢 Office Lunch**
- Main course: Equal split
- Extras: Only those who ordered
- Delivery: Split equally

## 🛠️ Technical Details

### **Built With**
- **Streamlit**: Modern Python web framework
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language

### **Key Components**
- `streamlit_bill.py`: Main application file
- `requirements.txt`: Python dependencies
- Zero session state for better performance
- Real-time calculations and validations

## 🏃‍♂️ Quick Start

### **Option 1: Run Locally**
```bash
# Clone the repository
git clone https://github.com/yourusername/Split_Bill_v2.git
cd Split_Bill_v2

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_bill.py
```

## 📱 How to Use

### **Step-by-Step Guide**

1. **Enter Participants**
   ```
   👥 People: Type names separated by commas
   Example: Alice, Bob, Carol
   ```

2. **Add Bill Items**
   ```
   � Items: Click cells to add item names and final prices
   Example: Food (₹800), Drinks (₹200), Tax (₹100)
   ```

3. **Assign Weights**
   - All weights start at 0 (nothing assigned initially)
   - Manually set weights for each person-item combination
   - Weight 0 = person doesn't pay for this item
   - Weight 1 = normal equal share
   - Weight 2+ = larger share (e.g., ate more)

4. **Track Payments**
   - Enter actual amounts paid by each person
   - View settlement calculations
   - Use WhatsApp summary or export detailed records

### **Export & Sharing Options** �

1. **WhatsApp Summary**
   - Copy-paste ready text for group chats
   - Includes all essential information
   - Perfect for quick sharing

2. **Detailed Text Export**
   - Comprehensive formatted summary
   - Complete weight matrix and calculations
   - Professional documentation

3. **CSV Export**
   - Spreadsheet-compatible format
   - Import into Excel or Google Sheets
   - Further analysis and record keeping

### **Pro Tips** 💡

- **Editing Cells**: Click → Type → Press Enter for best results
- **Starting Fresh**: All weights begin at 0 for intentional assignment
- **Complex Scenarios**: Use different weights for different consumption levels
- **Mobile Use**: App works great on phones for on-the-go splitting
- **Export Everything**: Download detailed records for your files

## 📊 Project Structure

```
Split_Bill_v2/
├── 📄 streamlit_bill.py             # Main application
├── 📄 requirements.txt              # Python dependencies  
├── 📄 README.md                     # This documentation
├── 📄 excel_bill.py                 # Excel processing utility
├── 📁 Bills/                        # Sample Excel files
│   ├── BillSplit.xlsx
│   ├── deadpool.xlsx
│   └── ...
└── 📄 runner.ipynb                  # Development notebook
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### **Ideas for Contributions**
- 🌍 Multi-currency support
-  Spending analytics and reports
- 🎨 Custom themes and styling
- 📱 Mobile app version
- 💾 Save/load bill templates
- 🔗 Integration with payment apps

## 📞 Support & Contact

- **Issues**: Report bugs or request features via GitHub Issues
- **Questions**: Use GitHub Discussions for general questions
- **Contributions**: Pull requests welcome!

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ and ☕ for hassle-free bill splitting!**
