--
-- PostgreSQL database dump
--

-- Dumped from database version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO pruebajr;

--
-- Name: bank_accounts; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.bank_accounts (
    id uuid NOT NULL,
    account_name character varying(512) NOT NULL,
    bank_name character varying(255) NOT NULL,
    account_number character varying(50) NOT NULL,
    current_balance numeric(24,4) NOT NULL,
    currency character varying(20) NOT NULL
);


ALTER TABLE public.bank_accounts OWNER TO pruebajr;

--
-- Name: expenses; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.expenses (
    id uuid NOT NULL,
    expense_date timestamp with time zone DEFAULT now() NOT NULL,
    description text,
    due_date timestamp with time zone,
    total_cost numeric(12,4) NOT NULL,
    recipient_account character varying(50),
    status integer NOT NULL,
    provider_id_fk uuid,
    created_by_fk uuid NOT NULL,
    approved_by_fk uuid,
    payment_fk uuid
);


ALTER TABLE public.expenses OWNER TO pruebajr;

--
-- Name: expenses_items; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.expenses_items (
    id uuid NOT NULL,
    expense_id uuid NOT NULL,
    item_name character varying(512) NOT NULL,
    description text,
    cost numeric(10,2)
);


ALTER TABLE public.expenses_items OWNER TO pruebajr;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.payments (
    id uuid NOT NULL,
    payment_date timestamp with time zone DEFAULT now(),
    total_amount numeric(10,2) NOT NULL,
    status integer NOT NULL,
    bank_account_id_fk uuid,
    created_by_fk uuid NOT NULL,
    approved_by_fk uuid,
    executed_by_fk uuid
);


ALTER TABLE public.payments OWNER TO pruebajr;

--
-- Name: providers; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.providers (
    id uuid NOT NULL,
    name character varying(512) NOT NULL,
    phone character varying(50),
    email character varying(255),
    address character varying(1024)
);


ALTER TABLE public.providers OWNER TO pruebajr;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.roles (
    id uuid NOT NULL,
    name character varying(512) NOT NULL,
    description character varying(512)
);


ALTER TABLE public.roles OWNER TO pruebajr;

--
-- Name: users; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username character varying(255),
    email character varying(255),
    password character varying(255),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO pruebajr;

--
-- Name: users_roles; Type: TABLE; Schema: public; Owner: pruebajr
--

CREATE TABLE public.users_roles (
    id uuid NOT NULL,
    user_id_fk uuid NOT NULL,
    role_id_fk uuid NOT NULL
);


ALTER TABLE public.users_roles OWNER TO pruebajr;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.alembic_version (version_num) FROM stdin;
3ded26d5450c
\.


--
-- Data for Name: bank_accounts; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.bank_accounts (id, account_name, bank_name, account_number, current_balance, currency) FROM stdin;
c4766567-fe30-47f9-af64-a65479ba0172	Tecnología	BBVA	6374856472	15837110.0000	MXN
8c68a841-8616-4185-826d-854fe0f716df	Equipment Purchases	Santander	748373849583	823384.0000	MXN
a3d4fa34-f2fd-4442-b91d-84146311b712	Utilities	HSBC	27382938273421	326984.0000	MXN
\.


--
-- Data for Name: expenses; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.expenses (id, expense_date, description, due_date, total_cost, recipient_account, status, provider_id_fk, created_by_fk, approved_by_fk, payment_fk) FROM stdin;
ebc5e02b-356e-481d-8728-ded7fc778476	2024-10-30 00:00:00-05	GTX 3060	2024-11-29 00:00:00-06	6534.2300	263748573647	0	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	\N
6020b057-e41e-4ad2-adcd-379f0d8d9379	2024-11-01 00:00:00-05	Teclado HP	2024-11-28 00:00:00-06	127.0000	263748573647	1	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	6393cfea-b76d-4fcd-9c4e-e53033a9352d
ce9894be-9e7f-414b-bd6d-abce81dfc8a8	2024-11-14 18:50:35.694-06	Compra de equipo de cómputo	2024-12-26 18:50:35.694-06	6500.0000	263746578273647584	1	\N	03a28b11-159f-4c96-ad34-cad6d4ac3d80	\N	1cb7eaba-30eb-48cd-be2d-609e0fac4fd9
533c6323-a21c-4312-8436-6d4e3a5b5042	2024-11-12 18:50:35.694-06	Compra de material de construcción	2024-12-29 18:50:35.694-06	2135.4500	263746578273647584	1	\N	03a28b11-159f-4c96-ad34-cad6d4ac3d80	\N	80c44776-86a8-468d-bf84-74644fa96c35
f7c0a19c-2fdc-42e5-b0a7-8b79d72b6fe0	2024-11-01 00:00:00-05	Material para pizarrón	2024-12-05 00:00:00-06	251.2300	263748573647	2	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	\N
57e57c71-006e-41f9-a3b7-aa26919ab013	2024-11-01 00:00:00-05	Cámara Web Logitech	2024-11-28 00:00:00-06	382.0000	263748573647	1	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	ff0f444f-ce4e-4771-82db-7d9201213d32
\.


--
-- Data for Name: expenses_items; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.expenses_items (id, expense_id, item_name, description, cost) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.payments (id, payment_date, total_amount, status, bank_account_id_fk, created_by_fk, approved_by_fk, executed_by_fk) FROM stdin;
1d23050b-b10c-46ec-83d4-294e84c38d41	2024-11-17 20:02:49.648055-06	6500.00	2	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	\N
80c44776-86a8-468d-bf84-74644fa96c35	2024-11-17 20:14:46.362249-06	2135.45	3	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0
ff0f444f-ce4e-4771-82db-7d9201213d32	2024-11-17 21:07:24.974373-06	382.00	3	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0
1cb7eaba-30eb-48cd-be2d-609e0fac4fd9	2024-11-17 22:49:55.573355-06	6500.00	0	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	\N
6393cfea-b76d-4fcd-9c4e-e53033a9352d	2024-11-17 22:48:49.741771-06	127.00	1	\N	8cb4cad4-ecf2-4a42-8c61-334fe9486df0	\N	\N
\.


--
-- Data for Name: providers; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.providers (id, name, phone, email, address) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.roles (id, name, description) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.users (id, username, email, password, created_at) FROM stdin;
8cb4cad4-ecf2-4a42-8c61-334fe9486df0	string	string	string	2024-11-15 15:09:35.981-06
4a9af578-2b0d-4e28-a620-9a06f5664135	string2	string2	string2	2024-11-15 21:11:25.305884-06
14798752-1a48-4c30-a40c-ea7e1190c295	string3	string3	string3	2024-11-15 15:14:08.559161-06
03a28b11-159f-4c96-ad34-cad6d4ac3d80	string4	string4	string4	2024-11-15 15:53:56.912-06
\.


--
-- Data for Name: users_roles; Type: TABLE DATA; Schema: public; Owner: pruebajr
--

COPY public.users_roles (id, user_id_fk, role_id_fk) FROM stdin;
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: bank_accounts bank_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.bank_accounts
    ADD CONSTRAINT bank_accounts_pkey PRIMARY KEY (id);


--
-- Name: expenses_items expenses_items_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses_items
    ADD CONSTRAINT expenses_items_pkey PRIMARY KEY (id);


--
-- Name: expenses expenses_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: providers providers_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.providers
    ADD CONSTRAINT providers_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: users_roles uix_user_role; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT uix_user_role UNIQUE (user_id_fk, role_id_fk);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_roles users_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_pkey PRIMARY KEY (id);


--
-- Name: expenses expenses_approved_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_approved_by_fk_fkey FOREIGN KEY (approved_by_fk) REFERENCES public.users(id);


--
-- Name: expenses expenses_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.users(id);


--
-- Name: expenses_items expenses_items_expense_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses_items
    ADD CONSTRAINT expenses_items_expense_id_fkey FOREIGN KEY (expense_id) REFERENCES public.expenses(id);


--
-- Name: expenses expenses_payment_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_payment_fk_fkey FOREIGN KEY (payment_fk) REFERENCES public.payments(id);


--
-- Name: expenses expenses_provider_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_provider_id_fk_fkey FOREIGN KEY (provider_id_fk) REFERENCES public.providers(id);


--
-- Name: payments payments_approved_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_approved_by_fk_fkey FOREIGN KEY (approved_by_fk) REFERENCES public.users(id);


--
-- Name: payments payments_bank_account_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_bank_account_id_fk_fkey FOREIGN KEY (bank_account_id_fk) REFERENCES public.bank_accounts(id);


--
-- Name: payments payments_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.users(id);


--
-- Name: payments payments_executed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_executed_by_fk_fkey FOREIGN KEY (executed_by_fk) REFERENCES public.users(id);


--
-- Name: users_roles users_roles_role_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_role_id_fk_fkey FOREIGN KEY (role_id_fk) REFERENCES public.roles(id);


--
-- Name: users_roles users_roles_user_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pruebajr
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_user_id_fk_fkey FOREIGN KEY (user_id_fk) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

