CREATE TABLE [dbo].[employee_account]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (100) NULL,
[number] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[is_default] [BIT] NULL DEFAULT 0,
[issuer] [varchar] (100) NULL,
[creation_date] [datetime] NULL,
[deactivation_date] [date] NULL,
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
