CREATE TABLE IF NOT EXISTS cameras (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(50),
    price_per_day INTEGER,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO cameras (brand, model, price_per_day) VALUES
('sony', 'A6400', 150000),
('canon', 'M50', 120000),
('fujifilm', 'EOS', 18000);