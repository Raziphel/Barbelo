
###########################################################################
######################## ADMINISTRATIVE / MODERATION ######################
###########################################################################

CREATE TABLE moderation (
    user_id bigint NOT NULL,
    adult boolean DEFAULT false,
    image_banned boolean DEFAULT false,
    PRIMARY KEY (user_id)
);

#############################################################################
############################## USER VALUES ##################################
#############################################################################

CREATE TABLE levels (
    user_id bigint NOT NULL,
    level integer NOT NULL DEFAULT 0,
    exp integer NOT NULL DEFAULT 0,
    last_xp timestamp,
    PRIMARY KEY (user_id)
);

CREATE TABLE currency (
    user_id bigint NOT NULL,
    coins integer DEFAULT 0,
    PRIMARY KEY (user_id)
);

CREATE TABLE daily (
    user_id bigint NOT NULL,
    daily integer NOT NULL DEFAULT 0,
    last_daily TIMESTAMP,
    PRIMARY KEY (user_id)
);

#############################################################################
########################## USER TRACK / RECORDS #############################
#############################################################################

CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    color integer,
    last_massage timestamp,
    PRIMARY KEY (user_id)
);

CREATE TABLE coins_record (
    user_id bigint NOT NULL,
    earned integer DEFAULT 0,
    spent integer DEFAULT 0,
    taxed integer DEFAULT 0,
    lost integer DEFAULT 0,
    stolen integer DEFAULT 0,
    gifted integer DEFAULT 0,
    given integer DEFAULT 0,
    PRIMARY KEY (user_id)
);

