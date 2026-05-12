# 1. Navigate to the project directory
cd /Users/sudhirpatil/code/opencodeweb

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate
# Your prompt will change to show (.venv) prefix

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up your API key
cp .env.example .env
# Open .env and replace the placeholder:
# ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# 6. Start the server
uvicorn app.main:app --port 8000 --reload

# 7. Open the UI in your browser
open http://localhost:8000
To deactivate the venv when done:


deactivate
To reactivate next time:


cd /Users/sudhirpatil/code/opencodeweb
source .venv/bin/activate
uvicorn app.main:app --port 8000 --reload
Quick test with curl (optional, to verify the API before using the UI):


# Create a test PySpark file
cat > /tmp/test_spark.py << 'EOF'
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet("/data/events")
result = df.collect()
small = spark.read.csv("/data/lookup")
joined = df.join(small, "id")
EOF

# Analyze it
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_path":"/tmp/test_spark.py","rules_prompt_path":"rules/default_rules.md"}'