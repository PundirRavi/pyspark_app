-- Create Dataset (if not exists - BigQuery doesn't support IF NOT EXISTS for schema)
-- This can be done via Terraform or manually

-- Table: patients
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.patients' (
  patient_id STRING NOT NULL,
  first_name STRING,
  last_name STRING,
  dob DATE,
  gender STRING,
  address STRING,
  city STRING,
  state STRING,
  zip_code STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Table: encounters
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.encounters' (
  encounter_id STRING NOT NULL,
  patient_id STRING,
  visit_type STRING,
  admission_time TIMESTAMP,
  discharge_time TIMESTAMP,
  location STRING,
  reason_code STRING,
  status STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Table: medications
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.medications' (
  medication_id STRING NOT NULL,
  patient_id STRING,
  drug_name STRING,
  dosage STRING,
  frequency STRING,
  start_date DATE,
  end_date DATE,
  prescribing_doc STRING
);

-- Table: observations
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.observations' (
  observation_id STRING NOT NULL,
  patient_id STRING,
  encounter_id STRING,
  type STRING,
  value FLOAT64,
  unit STRING,
  observed_at TIMESTAMP
);

-- Table: conditions
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.conditions' (
  condition_id STRING NOT NULL,
  patient_id STRING,
  code STRING,
  description STRING,
  start_date DATE,
  end_date DATE
);

-- Table: procedures
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.procedures' (
  procedure_id STRING NOT NULL,
  patient_id STRING,
  code STRING,
  description STRING,
  performed_at TIMESTAMP
);

-- Table: ehr_metadata
CREATE TABLE IF NOT EXISTS '${project_id}.${dataset_name}.ehr_metadata' (
  file_id STRING NOT NULL,
  file_name STRING,
  source_system STRING,
  upload_time TIMESTAMP,
  status STRING,
  error_message STRING
);
