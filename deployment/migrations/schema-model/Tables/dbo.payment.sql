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
