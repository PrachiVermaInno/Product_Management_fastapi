-- Drop existing tables (optional during development)
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS companies CASCADE;

-- ==========================
-- 1️⃣  Company Table
-- ==========================
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    descriptions TEXT
);

-- ==========================
-- 2️⃣  Category Table
-- ==========================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    company_id INT NOT NULL,
    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);

-- ==========================
-- 3️⃣  Product Table
-- ==========================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    stock INT DEFAULT 0,
    category_id INT NOT NULL,
    company_id INT NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_company_product
        FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);

-- ==========================
-- Optional Indexes
-- ==========================
CREATE INDEX idx_company_name ON companies(name);
CREATE INDEX idx_category_name ON categories(name);
CREATE INDEX idx_product_name ON products(name);
