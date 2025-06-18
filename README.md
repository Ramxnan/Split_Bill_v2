# 🧾 Interactive Bill Splitter

A modern, user-friendly Streamlit web application that makes splitting bills among friends, family, or colleagues incredibly easy and fair. No more complicated calculations or awkward conversations about who owes what!

🌐 **Live Demo**: [splitzy.streamlit.app](https://splitzy.streamlit.app)

## ✨ Features

### 🎯 **Smart Bill Splitting**
- **Weighted Distribution**: Split items proportionally based on who consumed what
- **Equal Split Buttons**: One-click equal distribution for shared items
- **Manual Control**: Fine-tune weights for complex splitting scenarios
- **Real-time Validation**: Instant feedback on splitting accuracy

### 🎨 **Intuitive User Experience**
- **Excel-like Interface**: Familiar grid editing with click-to-edit cells
- **Visual Feedback**: Color-coded validation (✅ balanced, ❌ mismatch)
- **Progressive Disclosure**: Clean interface that reveals options step-by-step
- **Mobile Friendly**: Works seamlessly on phones, tablets, and desktops

### 💰 **Complete Financial Tracking**
- **Item Details**: Track prices, quantities, and final costs
- **Payment Tracking**: Record who actually paid what
- **Settlement Calculator**: Automatic who-owes-whom calculations
- **Transaction Guide**: Step-by-step settlement instructions

### 🔧 **Smart Features**
- **Auto-calculations**: Real-time totals and splits
- **Balance Validation**: Ensures every rupee is accounted for
- **Weight Summaries**: Clear overview of distribution patterns
- **Reset Options**: Easy restart without losing session

## 🚀 How It Works

### 1. **Setup Your Group**
```
👥 People: Alice, Bob, Carol, David
🛒 Items: 🍕 Food, 🥤 Drinks, 💰 Tax, 🎯 Tips
```

### 2. **Enter Item Details**
- Click cells to edit prices and quantities
- Watch totals calculate automatically
- See your final bill amount

### 3. **Assign Weights**
- Use **Quick Split** buttons for equal sharing
- Manually edit weights for custom splits
- Weight 0 = doesn't pay, Weight 1 = normal share, Weight 2+ = larger share

### 4. **Track Payments**
- Enter who actually paid what amounts
- Get automatic settlement calculations
- Follow transaction guide to settle up

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
- `streamlit_bill_split_v2.py`: Main application file
- `requirements.txt`: Python dependencies
- Session state management for persistent data
- Real-time calculations and validations

### **Deployment**
- **Platform**: Streamlit Community Cloud
- **URL**: [splitc.streamlit.app](https://splitc.streamlit.app)
- **Auto-deployment**: Connected to GitHub repository
- **Zero-cost hosting**: Free for public repositories

## 🏃‍♂️ Quick Start

### **Option 1: Use Online (Recommended)**
Simply visit [splitc.streamlit.app](https://splitc.streamlit.app) - no installation needed!

### **Option 2: Run Locally**
```bash
# Clone the repository
git clone https://github.com/yourusername/Split_Bill_v2.git
cd Split_Bill_v2

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_bill_split_v2.py
```

## 📱 How to Use

### **Step-by-Step Guide**

1. **Enter Participants**
   ```
   👥 People: Type names separated by commas
   Example: Alice, Bob, Carol
   ```

2. **List Items/Categories**
   ```
   🛒 Items: Type items separated by commas  
   Example: Food, Drinks, Tax, Tips
   ```

3. **Generate Template**
   - Click "🚀 Generate Bill Split Template"
   - Interface expands with editing options

4. **Set Prices & Quantities**
   - Click any cell in the Item Details table
   - Type new values and press Enter
   - Watch totals update automatically

5. **Assign Weights**
   - Use "⚖️ Split [Item]" buttons for equal distribution
   - Or manually click cells to set custom weights
   - Weight 0 = person doesn't pay for this item
   - Weight 1 = normal equal share
   - Weight 2+ = larger share (e.g., ate more)

6. **Track Payments**
   - Enter actual amounts paid by each person
   - View settlement calculations
   - Follow transaction guide to settle up

### **Pro Tips** 💡

- **Editing Cells**: Click → Type → Press Enter for best results
- **Quick Equal Split**: Use the split buttons above each column
- **Complex Scenarios**: Mix equal splits with custom weights
- **Mobile Use**: App works great on phones for on-the-go splitting
- **Share Results**: Take screenshots of final tables to share

## 🔗 Deployment Information

The app is deployed on **Streamlit Community Cloud**:

- **URL**: [splitc.streamlit.app](https://splitc.streamlit.app)
- **Platform**: Streamlit Community Cloud (free tier)
- **Repository**: Connected to GitHub for auto-deployment
- **Updates**: Any code changes automatically deploy to the live app
- **Uptime**: 24/7 availability with Streamlit's infrastructure
- **SSL**: Secure HTTPS connection included

### **Deployment Benefits**
- ✅ **No Installation Required**: Works in any web browser
- ✅ **Always Updated**: Latest features automatically available
- ✅ **Cross-Platform**: Works on Windows, Mac, iOS, Android
- ✅ **Shareable**: Send the link to anyone
- ✅ **Fast Loading**: Optimized for quick access

## 📊 Project Structure

```
Split_Bill_v2/
├── 📄 streamlit_bill_split_v2.py    # Main application
├── 📄 requirements.txt              # Python dependencies  
├── 📄 README.md                     # This documentation
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
- 📧 Email/SMS sharing of results
- 📊 Spending analytics and reports
- 🎨 Custom themes and styling
- 📱 Mobile app version
- 💾 Save/load bill templates

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/Split_Bill_v2/issues)
- **Feature Requests**: Open an issue with the "enhancement" label
- **Questions**: Use GitHub Discussions

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ and ☕ for hassle-free bill splitting!**

*Last updated: December 2024*
