DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products (
    article_id VARCHAR(255) PRIMARY KEY,
    prod_name TEXT,
    cleaned_description TEXT,
    product_group_name VARCHAR(255),
    graphical_appearance_name VARCHAR(255),
    colour_group_name VARCHAR(255),
    section_name VARCHAR(255),
    garment_group_name VARCHAR(255),
    image_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);



COMMENT ON TABLE products IS 'Stores product metadata and prepared descriptions for the multimodal search engine.';