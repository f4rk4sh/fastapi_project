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
