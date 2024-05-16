

CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    last_bump timestamp,
    color integer,
    last_massage 
    PRIMARY KEY (user_id)
);

CREATE TABLE levels (
    user_id bigint NOT NULL,
    level integer NOT NULL DEFAULT 0,
    exp integer NOT NULL DEFAULT 0,
    last_xp timestamp,
    PRIMARY KEY (user_id)
);

CREATE TABLE daily (
    user_id bigint NOT NULL,
    last_daily TIMESTAMP,
    daily INT NOT NULL DEFAULT 0,
    premium BOOLEAN DEFAULT False,
    monthly TIMESTAMP,
    PRIMARY KEY (user_id)
);


CREATE TABLE coins (
    user_id bigint NOT NULL,
    coins integer DEFAULT 0,
    banked integer DEFAULT 0,
    earned integer DEFAULT 0,
    spent integer DEFAULT 0,
    taxed integer DEFAULT 0,
    lost integer DEFAULT 0,
    stolen integer DEFAULT 0,
    gifted integer DEFAULT 0,
    given integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE gems (
    user_id bigint NOT NULL,
    emerald integer DEFAULT 0,
    diamond integer DEFAULT 0,
    ruby integer DEFAULT 0,
    sapphire integer DEFAULT 0,
    amethyst integer DEFAULT 0,
    hellstone integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE moderation (
    user_id bigint NOT NULL,
    adult boolean DEFAULT false,
    child boolean DEFAULT false,
    muted boolean DEFAULT false,
    image_banned boolean DEFAULT false,
    PRIMARY KEY (user_id)
);


CREATE TABLE thievery (
    user_id BIGINT NOT NULL,
    level boolean DEFAULT false,
    last_steal TIMESTAMP,
    PRIMARY KEY (user_id)
);
