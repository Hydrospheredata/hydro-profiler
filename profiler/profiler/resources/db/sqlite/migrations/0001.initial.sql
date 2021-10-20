-- CREATE TABLE "untitled_table_7" ("id" integer,"model" varchar NOT NULL, PRIMARY KEY (id));
CREATE TABLE "models" ("name" varchar NOT NULL,"version" int NOT NULL,"contract" text NOT NULL);
CREATE TABLE "reports" ("model_name" varchar, "model_version" varchar NOT NULL, "batch_name" varchar NOT NULL, "report" text NOT NULL);
CREATE TABLE "metrics" ("model_name" varchar NOT NULL,"model_version" text NOT NULL DEFAULT '[]', "metrics" text NOT NULL);
CREATE TABLE "aggregations" ("model_name" varchar NOT NULL,"model_version" integer NOT NULL,"batch_name" varchar NOT NULL,"aggregation" text NOT NULL);
