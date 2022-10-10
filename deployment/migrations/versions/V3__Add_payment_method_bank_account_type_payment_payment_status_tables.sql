CREATE TABLE [dbo].[payment_status]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[payment_status] ADD CONSTRAINT [PK__payment_status__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_payment_status_id] ON [dbo].[payment_status] ([id])
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
[edrpou] [varchar] (50) NULL,
[mfo] [varchar] (50) NULL,
[iban] [varchar] (50) NULL,
[card] [varchar] (50) NULL,
[account_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[bank] ADD CONSTRAINT [PK__bank__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_bank_id] ON [dbo].[bank] ([id])
GO
ALTER TABLE [dbo].[bank] ADD CONSTRAINT [FK__bank__account_type__id] FOREIGN KEY ([account_type_id]) REFERENCES [dbo].[account_type] ([id]) ON DELETE CASCADE
GO

CREATE TABLE [dbo].[payment_method]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[is_default] [BIT] NULL DEFAULT 0,
[is_active] [BIT] NULL DEFAULT 0,
[employee_id] [int] NULL,
[bank_id] [int] NULL
)
GO
ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [PK__payment_method__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_payment_method_id] ON [dbo].[payment_method] ([id])
GO
ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [FK__payment_method__employee__id] FOREIGN KEY ([employee_id]) REFERENCES [dbo].[employee] ([id]) ON DELETE CASCADE
GO
ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [FK__payment_method__bank__id] FOREIGN KEY ([bank_id]) REFERENCES [dbo].[bank] ([id]) ON DELETE CASCADE
GO

CREATE TABLE [dbo].[payment]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[amount] [bigint] NULL,
[creation_date] [date] NULL,
[execution_date] [date] NULL,
[employee_id] [int] NULL,
[payment_status_id] [int] NULL,
[payment_method_id] [int] NULL
)
GO
ALTER TABLE [dbo].[payment] ADD CONSTRAINT [PK__payment__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_payment_id] ON [dbo].[payment] ([id])
GO
ALTER TABLE [dbo].[payment] ADD CONSTRAINT [FK__payment__employee__id] FOREIGN KEY ([employee_id]) REFERENCES [dbo].[employee] ([id])
GO
ALTER TABLE [dbo].[payment] ADD CONSTRAINT [FK__payment__payment_status__id] FOREIGN KEY ([payment_status_id]) REFERENCES [dbo].[payment_status] ([id]) ON DELETE CASCADE
GO
ALTER TABLE [dbo].[payment] ADD CONSTRAINT [FK__payment__payment_method__id] FOREIGN KEY ([payment_method_id]) REFERENCES [dbo].[payment_method] ([id]) ON DELETE CASCADE
GO