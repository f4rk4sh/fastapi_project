CREATE TABLE [dbo].[payment_status_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[payment_status_type] ADD CONSTRAINT [PK__payment_status_type__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_payment_status_type_id] ON [dbo].[payment_status_type] ([id])
GO

CREATE TABLE [dbo].[account_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[account_type] ADD CONSTRAINT [PK__account_type__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_account_type_id] ON [dbo].[account_type] ([id])
GO

CREATE TABLE [dbo].[bank]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL,
[mfo] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[creation_date] [datetime] NULL,
[deactivation_date] [datetime] NULL
)
GO
ALTER TABLE [dbo].[bank] ADD CONSTRAINT [PK__bank__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_bank_id] ON [dbo].[bank] ([id])
GO

CREATE TABLE [dbo].[employer_payment_method]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[iban] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[creation_date] [datetime] NULL,
[deactivation_date] [datetime] NULL,
[employer_id] [int] NULL,
[bank_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [PK__employer_payment_method__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_payment_method_id] ON [dbo].[employer_payment_method] ([id])
GO
ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [FK__employer_payment_method__employer__id] FOREIGN KEY ([employer_id]) REFERENCES [dbo].[employer] ([id]) ON DELETE CASCADE
GO
ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [FK__employer_payment_method__bank__id] FOREIGN KEY ([bank_id]) REFERENCES [dbo].[bank] ([id]) ON DELETE CASCADE
GO


CREATE TABLE [dbo].[employee_account]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (100) NULL,
[number] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[is_default] [BIT] NULL DEFAULT 0,
[card_issuer] [varchar] (100) NULL,
[creation_date] [datetime] NULL,
[deactivation_date] [datetime] NULL,
[employee_id] [int] NULL,
[account_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employee_account] ADD CONSTRAINT [PK__employee_account__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_account_id] ON [dbo].[employee_account] ([id])
GO
ALTER TABLE [dbo].[employee_account] ADD CONSTRAINT [FK__employee_account__employee__id] FOREIGN KEY ([employee_id]) REFERENCES [dbo].[employee] ([id]) ON DELETE CASCADE
GO
ALTER TABLE [dbo].[employee_account] ADD CONSTRAINT [FK__employee_account__account_type__id] FOREIGN KEY ([account_type_id]) REFERENCES [dbo].[account_type] ([id])
GO

CREATE TABLE [dbo].[payment_history]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[amount] [bigint] NULL,
[creation_date] [datetime] NULL,
[employee_account_id] [int] NULL,
[employer_payment_method_id] [int] NULL,
[payment_status_type_id] [int] NULL,
)
GO
ALTER TABLE [dbo].[payment_history] ADD CONSTRAINT [PK__payment_history__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_payment_history_id] ON [dbo].[payment_history] ([id])
GO
ALTER TABLE [dbo].[payment_history] ADD CONSTRAINT [FK__payment_history__employee_account__id] FOREIGN KEY ([employee_account_id]) REFERENCES [dbo].[employee_account] ([id])
GO
ALTER TABLE [dbo].[payment_history] ADD CONSTRAINT [FK__payment_history__employer_payment_method__id] FOREIGN KEY ([employer_payment_method_id]) REFERENCES [dbo].[employer_payment_method] ([id])
GO
ALTER TABLE [dbo].[payment_history] ADD CONSTRAINT [FK__payment_history__payment_status_type__id] FOREIGN KEY ([payment_status_type_id]) REFERENCES [dbo].[payment_status_type] ([id])
GO