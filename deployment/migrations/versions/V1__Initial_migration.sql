CREATE TABLE [dbo].[role]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[role] ADD CONSTRAINT [PK__role__3213E83F63EB5C83] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_role_id] ON [dbo].[role] ([id])
GO

CREATE TABLE [dbo].[status_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[status_type] ADD CONSTRAINT [PK__status_t__3213E83F8AE383FD] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_status_type_id] ON [dbo].[status_type] ([id])
GO

CREATE TABLE [dbo].[employer_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[employer_type] ADD CONSTRAINT [PK__employer__3213E83F217C961A] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_type_id] ON [dbo].[employer_type] ([id])
GO

CREATE TABLE [dbo].[user]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[email] [varchar] (50) NULL,
[password] [varchar] (100) NULL,
[phone] [varchar] (50) NULL,
[creation_date] [datetime] NULL,
[activation_date] [datetime] NULL,
[role_id] [int] NULL,
[status_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [PK__user__3213E83F0B6C9234] PRIMARY KEY CLUSTERED ([id])
GO
CREATE UNIQUE NONCLUSTERED INDEX [ix_user_email] ON [dbo].[user] ([email])
GO
CREATE NONCLUSTERED INDEX [ix_user_id] ON [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__role_id__2EB0D91F] FOREIGN KEY ([role_id]) REFERENCES [dbo].[role] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__status_typ__2FA4FD58] FOREIGN KEY ([status_type_id]) REFERENCES [dbo].[status_type] ([id])
GO

CREATE TABLE [dbo].[employer]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (100) NULL,
[address] [varchar] (100) NULL,
[edrpou] [varchar] (50) NULL,
[expire_contract_date] [date] NULL,
[salary_date] [date] NULL,
[prepayment_date] [date] NULL,
[user_id] [int] NULL,
[employer_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [PK__employer__3213E83FC1B8210B] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_edrpou] ON [dbo].[employer] ([edrpou])
GO
CREATE NONCLUSTERED INDEX [ix_employer_id] ON [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__employ__33758E3C] FOREIGN KEY ([employer_type_id]) REFERENCES [dbo].[employer_type] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__user_i__32816A03] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO

CREATE TABLE [dbo].[employee]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[fullname] [varchar] (100) NULL,
[passport] [varchar] (50) NULL,
[tax_id] [varchar] (50) NULL,
[birth_date] [date] NULL,
[user_id] [int] NULL,
[employer_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [PK__employee__3213E83F08D51DC3] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_id] ON [dbo].[employee] ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_passport] ON [dbo].[employee] ([passport])
GO
CREATE NONCLUSTERED INDEX [ix_employee_tax_id] ON [dbo].[employee] ([tax_id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__employ__37461F20] FOREIGN KEY ([employer_id]) REFERENCES [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__user_i__3651FAE7] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO

CREATE TABLE [dbo].[session]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[token] [varchar] (100) NULL,
[creation_date] [datetime] NULL
)
GO
ALTER TABLE [dbo].[session] ADD CONSTRAINT [PK__session__3213E83F51D5D72D] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_session_id] ON [dbo].[session] ([id])
GO