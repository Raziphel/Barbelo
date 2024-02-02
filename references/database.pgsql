

CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    last_bump timestamp,
    color integer,
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


CREATE TABLE currency (
    user_id bigint NOT NULL,
    coins integer DEFAULT 500,
    coins_earned integer DEFAULT 0,
    last_coin TIMESTAMP,
    xp integer DEFAULT 1,
    xp_earned integer DEFAULT 0,
    last_xp TIMESTAMP,
    lot_tickets Integer DEFAULT 0,
    PRIMARY KEY (user_id)
);

