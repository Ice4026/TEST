def main():
    import DotaMax
    info = DotaMax.DotaMax("106777328")
    info.updateMySQL()
    for i in info.recentMatch():
        print(list(i)),

if __name__ == '__main__':
    main()
