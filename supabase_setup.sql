-- ============================================================
-- Advaith Industries — Supabase Database Setup
-- Run this in your Supabase SQL Editor:
-- https://srksfyadtzgojeyssdcf.supabase.co (Project Settings → SQL Editor)
-- ============================================================


-- ── Products table ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.products (
    id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name        text NOT NULL,
    description text,
    category    text,
    price       numeric(12, 2),
    image_url   text,
    in_stock    boolean DEFAULT true,
    created_at  timestamptz DEFAULT now()
);

-- Enable Row Level Security and allow public reads
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can read products"
    ON public.products FOR SELECT
    USING (true);


-- ── Contacts table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.contacts (
    id         uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name       text NOT NULL,
    company    text,
    email      text NOT NULL,
    message    text NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security and allow public inserts only
ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can insert contacts"
    ON public.contacts FOR INSERT
    WITH CHECK (true);


-- ── Sample product data ───────────────────────────────────────
INSERT INTO public.products (name, description, category, price, in_stock) VALUES
    ('Precision Brass Fittings',      'High-conductivity brass fittings machined to ±0.01mm tolerances for hydraulic and pneumatic systems.', 'Fittings',    149.00, true),
    ('Industrial Steel Shafts',       'Hardened alloy steel shafts with ground finish, suitable for high-load rotary applications.',            'Shafts',      320.00, true),
    ('Custom Injection Mold Tooling', 'Multi-cavity injection mold tooling manufactured from P20 tool steel with long-run durability.',         'Tooling',    2400.00, true),
    ('Aluminum Enclosures',           'Anodized aluminium enclosures with CNC-machined apertures, IP65-rated for industrial environments.',     'Enclosures',  215.00, true),
    ('Industrial Resin Components',   'Glass-fibre reinforced resin components rated for continuous service at up to 180°C.',                  'Plastics',     98.00, true),
    ('Heavy Duty Fasteners',          'Grade 12.9 metric fasteners manufactured from alloy steel with zinc-nickel plating.',                   'Fasteners',    42.00, true);
