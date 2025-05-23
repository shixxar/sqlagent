# Data Analysis Agent

A sophisticated multi-agent system built with ADK (Agent Development Kit) that processes natural language questions, converts them to SQL queries, retrieves data from the Chinook database, and provides intelligent responses with optional data visualization capabilities.

## 🚀 Features

- **Natural Language to SQL**: Converts user questions into optimized SQL queries
- **Multi-Agent Architecture**: Coordinated agents for query generation, data retrieval, and response formation
- **Data Visualization**: Automatic plot generation and data visualization using BQML agent
- **Chinook Database Integration**: Works seamlessly with the popular Chinook sample database
- **Web Interface**: Easy-to-use web interface via ADK Web
- **Intelligent Response Generation**: Contextual and coherent answers based on retrieved data

## 📋 Prerequisites

- Python 3.8 or higher
- ADK (Agent Development Kit) installed
- Web browser for accessing the interface
- Git (for cloning the repository)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/shixxar/sqlagent>
cd <sqlagent>
```

### 2. Install Dependencies

Install all required dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 3. Verify ADK Installation

Ensure ADK is properly installed and accessible:

```bash
adk --version
```

If ADK is not installed, follow the official ADK installation guide.

### 4. Database Setup

The project uses the Chinook database. Ensure the database file is present in the project directory or update the configuration to point to the correct database location.

## 🚀 Usage

### Starting the Application

1. **Launch ADK Web Interface**:
   ```bash
   adk web
   ```

2. **Access the Application**:
   - Open your web browser
   - Navigate to the local URL provided by ADK (typically `http://localhost:8000`)

### Using the SQL Agent

1. **Input Your Question**: 
   - Enter your natural language question in the provided interface
   - Example: "What are the top 10 best-selling albums?"
   - Example: "Show me the total sales by country"

2. **Agent Processing Flow**:
   - **Query Agent**: Converts your question into an optimized SQL query
   - **Data Retrieval**: Executes the query against the Chinook database
   - **Response Agent**: Processes the retrieved data and generates a coherent answer
   - **Visualization Agent** (optional): Creates relevant plots and charts

3. **View Results**:
   - Text-based answers with context and insights
   - Data visualizations and charts (when applicable)
   - Raw data tables for detailed analysis

## 🏗️ Architecture

### Multi-Agent System

```
User Question → Query Generation Agent → Database → Data Processing Agent → Response Agent
                                                           ↓
                                               Visualization Agent (BQML)
```

1. **Query Generation Agent**: 
   - Analyzes natural language input
   - Generates appropriate SQL queries
   - Optimizes for Chinook database schema

2. **Data Retrieval System**:
   - Executes SQL queries safely
   - Handles database connections
   - Returns structured data

3. **Response Generation Agent**:
   - Processes retrieved data
   - Generates contextual responses
   - Provides insights and summaries

4. **Visualization Agent (BQML)**:
   - Creates appropriate charts and plots
   - Handles different data types
   - Generates interactive visualizations

## 📊 Chinook Database

The Chinook database represents a digital media store with the following key tables:

- **Albums**: Album information
- **Artists**: Artist details
- **Customers**: Customer data
- **Employees**: Employee information
- **Genres**: Music genres
- **Invoices**: Sales transactions
- **InvoiceLines**: Detailed invoice items
- **MediaTypes**: Media format types
- **Playlists**: User playlists
- **Tracks**: Individual song information

### Sample Questions You Can Ask

- "Who are the top 5 customers by total purchases?"
- "What's the most popular genre by sales?"
- "Show me monthly sales trends for 2023"
- "Which employee has the highest sales performance?"
- "What are the longest tracks in the database?"
- "Display the distribution of customers by country"

## 🔧 Configuration

### Database Configuration

Update database connection settings in your configuration file:

```python
DATABASE_CONFIG = {
    'path': 'chinook.db',
    'type': 'sqlite'
}
```

### Agent Configuration

Customize agent behavior by modifying the agent configuration files in the `config/` directory.

## 📝 Project Structure

```
project-root/
│
├── agents/
│   ├── query_agent.py
│   ├── response_agent.py
│   └── visualization_agent.py
│
├── config/
│   ├── agent_config.yaml
│   └── database_config.yaml
│
├── data/
│   └── chinook.db
│
├── utils/
│   ├── database.py
│   └── query_optimizer.py
│
├── requirements.txt
├── main.py
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

1. **ADK Not Found**:
   ```bash
   pip install adk
   ```

2. **Database Connection Issues**:
   - Verify the Chinook database file exists
   - Check file permissions
   - Ensure the path in configuration is correct

3. **Port Already in Use**:
   ```bash
   adk web --port 8001
   ```

4. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

### Performance Tips

- Use specific questions for better SQL generation
- Limit result sets for large queries
- Cache frequently requested data
- Optimize database indexes for common queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ADK team for the Agent Development Kit
- Chinook Database creators for the sample dataset
- Open source community for various libraries and tools

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review ADK documentation
3. Open an issue in the GitHub repository
4. Contact the development team

## 🔄 Version History

- **v1.0.0**: Initial release with basic SQL agent functionality
- **v1.1.0**: Added visualization capabilities
- **v1.2.0**: Enhanced response generation and error handling

---

**Happy querying! 🎵📊**
