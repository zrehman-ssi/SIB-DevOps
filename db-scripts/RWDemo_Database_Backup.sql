PGDMP     ;    %        	        w            RWDemo    11.4    11.3     �
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            �
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            �
           1262    16393    RWDemo    DATABASE     �   CREATE DATABASE "RWDemo" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "RWDemo";
             postgres    false            �            1259    16394    Logins    TABLE     �   CREATE TABLE public."Logins" (
    username character varying(200),
    password character varying(200),
    "fullName" character varying,
    "mobileNo" character varying,
    address character varying
);
    DROP TABLE public."Logins";
       public         postgres    false            �
          0    16394    Logins 
   TABLE DATA               W   COPY public."Logins" (username, password, "fullName", "mobileNo", address) FROM stdin;
    public       postgres    false    196   �       �
   �   x�}�M
� ��3��Mz �&��B��f@S]X�~��MR���9��9R0�0�)oe�U��\��㲱�۾_Lz�������oe���.�����ev���,�>8�`��DzB:g�r����x��v��U	Q��Ū`} O�)jQ%+�xB�Yo,     