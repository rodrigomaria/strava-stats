# Build stage
FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --root-user-action=ignore --upgrade pip \
    && pip install --root-user-action=ignore --no-cache-dir --no-warn-script-location --user -r requirements.txt

# Runtime stage
FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["tail", "-f", "/dev/null"]
