import pandas as pd
import os
import re
import time
import schedule
import logging
from datetime import datetime 
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

# Create Logging Configuartion

# Create log directory if not exists
os.makedirs('../log',exist_ok=True)

# Dynamic daily log file
log_filename = f"../log/etl_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename = log_filename,
    level = logging.DEBUG,
    filemode = 'a',
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

# Load Environment Veriables
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create Database Connection
DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URI)

# File Directory Configuration
data_dir = '../dataset/raw/shopping_behavior_updated.csv'

# ETL job Creation
def extract():
    try:
        try:
            df = pd.read_csv(data_dir, encoding='utf-8')
            logging.info(f"File extracted (UTF-8) - {len(df)} rows")
        except UnicodeDecodeError:
            df = pd.read_csv(data_dir, encoding='latin1')
            logging.warning("File reloaded with Latin1 encoding")
            logging.info(f"File extracted (Latin1) - {len(df)} rows")
        return df

    except FileNotFoundError:
        logging.error(f"File not found: {data_dir}")
        raise
        
    except Exception as e:
        logging.error(f'Error in File Extraction: {e}')
        raise

def transform(df):
    try:
        # Convert categorical columns
        category_columns = [
         "Gender",
            "Item Purchased",
            "Category",
            "Location",
            "Size",
            "Color",
            "Season",
            "Subscription Status",
            "Shipping Type",
            "Discount Applied",
            "Promo Code Used",
            "Payment Method",
            "Frequency of Purchases"
        ]

        for col in category_columns:
            if col in df.columns:
                df[col] = df[col].astype("category")
        
        
        # ---------------------------------------
        # Optimize numeric columns
        # ---------------------------------------

        numeric_cols = ["Customer ID","Age","Purchase Amount (USD)","Previous Purchases"]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype('int32')

        # ----------------------------------------------------
        # Rename 'Purchase Amount (USD)' column if it exists
        # ----------------------------------------------------
        if 'Purchase Amount (USD)' in df.columns:
            df.rename(columns={'Purchase Amount (USD)': 'Purchase Amount'}, inplace=True)
        
        # Create Age Group column based on customer age
        def age_group(age):
            """Categorize age values into human-readable segments."""
            if 18 <= age <= 25:
                return 'Young_Adult'
            elif 26 <= age <= 35:
                return 'Adult'
            elif 36 <= age <= 45:
                return 'Senior_Adult'
            elif 46 <= age <= 60:
                return 'Middle_Aged'
            elif age > 60:
                return 'Senior'
            else:
                return 'Teenager'
        
        if 'Age' in df.columns:
            df['Age_Group'] = df['Age'].apply(age_group)
        
        # Map frequency labels to numeric day equivalents
        frequency_mapping = {
            'Fortnightly': 14,
            'Weekly': 7,
            'Monthly': 30,
            'Quarterly': 90,
            'Bi-Weekly': 14,
            'Annually': 365,
            'Every 3 Months': 90
        }
    
        if 'Frequency of Purchases' in df.columns:
            df['Purchase_Frequency_Days'] = df['Frequency of Purchases'].map(frequency_mapping)
        else:
            logging.warning("No 'Frequency of Purchases' column found for mapping.")

    
        # Drop unnecessary or redundant columns 
        if 'Promo Code Used' in df.columns:
            df.drop('Promo Code Used', axis=1, inplace=True)
      
        # Clean and normalize column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
          
        # Log transformation completion  
        logging.info("✅ Data transformation complete.")
        
        # Return the transformed dataframe
        return df
    

    # Exception handling with logging
    except Exception as e:
        logging.error(f"File Transformation failed: {e}")
        raise


def load(df):
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS customers_shopping_behavior;"))
        df.to_sql(
            name='shopping_behavior',
            con=engine,
            schema='customers_shopping_behavior',
            if_exists='replace',
            index=False
        )
        logging.info(f"Loaded {len(df)} rows into PostgreSQL.")
    except Exception as e:
        logging.error(f"File Loading failed: {e}")
        raise

    # Upload new Updated DataFrame into dataset as .csv
    try:
        df.to_csv('../dataset/processed/updated_customer_shopping_behaviour_data.csv',index = False)
        logging.info(f"Loaded {len(df)} rows into PostgreSQL.")
    except Exception as e:
        logging.error(f"File Loading failed as processed csv: {e}")

        
def etl_run():
    try:
        df = extract()
        df = transform(df)
        load(df)
        logging.info("===== ETL job completed successfully =====")
    except Exception as e:
        logging.critical(f"ETL job crashed: {e}")
        raise

# Main Execution And Seduling
if __name__ == '__main__':
    # Run ETL job immediately when script starts
    etl_run()

    # Schedule ETL job to run daily at 2:00 AM automatically
    schedule.every().day.at("03:00").do(etl_run)
    logging.info("Scheduler started. Waiting for daily ETL jobs...")

    # Keep script running continuously to check pending jobs
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep 1 minute between schedule checks