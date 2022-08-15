CREATE TABLE [dbo].[status_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[status_type] ADD CONSTRAINT [PK__status_t__3213E83FCF5FD229] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_status_type_id] ON [dbo].[status_type] ([id])
GO
