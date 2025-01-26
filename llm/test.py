from openai import OpenAI


client = OpenAI(
    organization='org-luqBLIGrKRcCm3mNahUny8tR',
    project='proj_sdCnoxZvLzWH9qYdCPwPUXem',
)

completion = client.chat.completions.create(
#    model="gpt-4o",
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Who is Trump?."
        }
    ]
)

print(completion.choices[0].message)
#print(response._request_id)