--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: files_reader; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files_reader (
    "Type" text,
    "Name" text
);


ALTER TABLE public.files_reader OWNER TO postgres;

--
-- Data for Name: files_reader; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.files_reader ("Type", "Name") FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

